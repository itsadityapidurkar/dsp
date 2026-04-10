from __future__ import annotations

import json
import re
from collections import Counter
from io import BytesIO

from docx import Document
from pypdf import PdfReader

from app.repositories.analytics import AnalyticsRepository
from app.schemas.resume import LearningResource, RecommendedRole, ResumeAnalysisResponse
from app.services.gemini_service import GeminiService


RESOURCE_MAP = {
    "Python": ("Python Learning Path", "https://www.python.org/about/gettingstarted/"),
    "SQL": ("SQL Tutorial", "https://www.w3schools.com/sql/"),
    "Power BI": ("Power BI Training", "https://learn.microsoft.com/power-bi/"),
    "Tableau": ("Tableau Learning", "https://www.tableau.com/learn/training"),
    "AWS": ("AWS Skill Builder", "https://skillbuilder.aws/"),
    "Docker": ("Docker Docs", "https://docs.docker.com/get-started/"),
    "Kubernetes": ("Kubernetes Basics", "https://kubernetes.io/docs/tutorials/kubernetes-basics/"),
}


class ResumeService:
    def __init__(self, repository: AnalyticsRepository, gemini_service: GeminiService | None = None):
        self.repository = repository
        self.gemini = gemini_service or GeminiService()
        self.skill_dictionary = {skill.lower(): skill for skill, _ in self.repository.top_skills({}, limit=500)}

    def parse_resume(self, filename: str, file_bytes: bytes) -> str:
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(file_bytes))
            return " ".join(page.extract_text() or "" for page in reader.pages)
        if filename.lower().endswith(".docx"):
            document = Document(BytesIO(file_bytes))
            return " ".join(paragraph.text for paragraph in document.paragraphs)
        raise ValueError("Unsupported file type")

    def analyze_resume(self, filename: str, file_bytes: bytes) -> ResumeAnalysisResponse:
        text = self.parse_resume(filename, file_bytes)
        clean_text = re.sub(r"\s+", " ", text.lower()).strip()
        if not clean_text:
            raise ValueError("Resume content is empty")
        candidate_skills = self.extract_skills(clean_text)
        recommendations = self.rank_roles(candidate_skills, clean_text)
        top_role = recommendations[0]["role"] if recommendations else ""
        top_role_skills = [skill for skill, _ in self.repository.top_skills_for_role(top_role, limit=12)]
        missing_skills = sorted(skill for skill in top_role_skills if skill not in candidate_skills)
        suggestions = self.build_suggestions(missing_skills)
        resources = self.build_resources(missing_skills)
        fallback_insight = (
            f"You already show strength in {', '.join(candidate_skills[:3]) or 'foundational skills'}. "
            f"Prioritize {', '.join(missing_skills[:3]) or 'role-specific tools'} to improve role fit."
        )
        insight = self.gemini.generate_text(
            f"Give a short resume fit insight for a candidate targeting {top_role or 'job market roles'}.",
            fallback=fallback_insight,
        )
        profile_summary = self._profile_summary(recommendations, candidate_skills)
        match_score = recommendations[0]["score"] if recommendations else 0
        return ResumeAnalysisResponse(
            match_score=match_score,
            recommended_roles=[RecommendedRole(**item) for item in recommendations[:5]],
            your_skills=candidate_skills,
            missing_skills=missing_skills,
            suggestions=suggestions,
            learning_resources=resources,
            insight=insight,
            profile_summary=profile_summary,
        )

    def extract_skills(self, text: str) -> list[str]:
        found = []
        aliases = {"js": "javascript", "py": "python", "power bi": "power bi"}
        for alias, normalized in aliases.items():
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", text):
                found.append(self.skill_dictionary.get(normalized, normalized.title()))
        for lowered, original in self.skill_dictionary.items():
            if re.search(rf"(?<![a-z0-9]){re.escape(lowered)}(?![a-z0-9])", text):
                found.append(original)
        return sorted(set(found))

    def rank_roles(self, candidate_skills: list[str], text: str) -> list[dict]:
        roles = self.repository.list_roles()
        candidate_skill_set = set(candidate_skills)
        candidate_exp = self._infer_candidate_experience(text)
        results = []
        for role in roles:
            role_skills = {skill for skill, _ in self.repository.top_skills_for_role(role, limit=15)}
            if not role_skills:
                continue
            overlap = len(candidate_skill_set.intersection(role_skills)) / len(role_skills)
            role_experience = self.repository.experience_distribution_for_role(role)
            experience_score = self._experience_alignment(candidate_exp, role_experience)
            category_score = 1.0 if any(token in role.lower() for token in ["data", "analyst", "engineer", "developer", "security"]) else 0.6
            score = round((0.7 * overlap + 0.2 * experience_score + 0.1 * category_score) * 100)
            results.append({"role": role, "score": score})
        return sorted(results, key=lambda item: item["score"], reverse=True)[:5]

    def build_suggestions(self, missing_skills: list[str]) -> list[str]:
        suggestions = []
        for skill in missing_skills[:3]:
            suggestions.append(f"Build evidence of {skill} through one project and a resume bullet tied to outcomes.")
        if not suggestions:
            suggestions.append("Your current skill mix already aligns well. Strengthen project depth and measurable outcomes.")
        return suggestions

    def build_resources(self, missing_skills: list[str]) -> list[LearningResource]:
        resources = []
        for skill in missing_skills[:5]:
            title, url = RESOURCE_MAP.get(skill, (f"{skill} Learning Resource", "https://roadmap.sh/"))
            resources.append(LearningResource(skill=skill, title=title, url=url))
        return resources

    def _infer_candidate_experience(self, text: str) -> str:
        if re.search(r"\bintern|internship|student\b", text):
            return "Intern"
        if re.search(r"\bjunior|entry\b", text):
            return "Entry"
        if re.search(r"\bsenior|lead|principal\b", text):
            return "Senior"
        return "Mid"

    def _experience_alignment(self, candidate_exp: str, role_experience: list[tuple[str, int]]) -> float:
        if not role_experience:
            return 0.5
        leading = role_experience[0][0]
        if leading == candidate_exp:
            return 1.0
        if {leading, candidate_exp} <= {"Entry", "Intern"}:
            return 0.8
        if {leading, candidate_exp} <= {"Mid", "Senior"}:
            return 0.8
        return 0.5

    def _profile_summary(self, recommendations: list[dict], candidate_skills: list[str]) -> str:
        if not recommendations:
            return "Profile needs clearer market signals before role matching is reliable."
        top_role = recommendations[0]["role"]
        if recommendations[0]["score"] >= 75:
            return f"Strong market-aligned profile for {top_role} with clear foundational skill coverage."
        return f"Emerging profile with strongest alignment toward {top_role}; adding targeted tools will improve fit."
