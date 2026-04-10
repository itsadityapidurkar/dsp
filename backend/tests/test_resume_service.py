from app.services.resume_service import ResumeService


class StubRepository:
    def top_skills(self, filters, limit=500):
        return [("Python", 10), ("SQL", 8), ("Power BI", 6), ("Docker", 5)]

    def top_skills_for_role(self, role, limit=15):
        if role == "Data Analyst":
            return [("Python", 8), ("SQL", 7), ("Power BI", 6)]
        return [("Docker", 7), ("Python", 6)]

    def list_roles(self):
        return ["Data Analyst", "Backend Engineer"]

    def experience_distribution_for_role(self, role):
        return [("Entry", 30)]


class StubGemini:
    def generate_text(self, prompt: str, fallback: str) -> str:
        return fallback


class ResumeServiceHarness(ResumeService):
    def parse_resume(self, filename: str, file_bytes: bytes) -> str:
        return file_bytes.decode("utf-8")


def test_resume_analysis_scores_roles():
    service = ResumeServiceHarness(StubRepository(), StubGemini())
    result = service.analyze_resume("resume.pdf", b"Python SQL dashboard reporting")
    assert result.match_score >= 50
    assert result.recommended_roles[0].role == "Data Analyst"
    assert "Power BI" in result.missing_skills
