from __future__ import annotations

from statistics import mean

from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import CompareRolePanel, CompareRolesResponse, RoleOverviewResponse
from app.schemas.common import SalaryRange
from app.services.gemini_service import GeminiService
from app.utils.formatting import demand_level, summarize_levels, summarize_remote, top_label


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository, gemini_service: GeminiService | None = None):
        self.repository = repository
        self.gemini = gemini_service or GeminiService()

    def top_skills(self, filters: dict, limit: int = 15) -> list[dict]:
        return [{"skill": skill, "demand_score": count} for skill, count in self.repository.top_skills(filters, limit)]

    def category_distribution(self, filters: dict) -> list[dict]:
        return [{"category": category, "value": count} for category, count in self.repository.top_categories(filters)]

    def top_roles(self, filters: dict, limit: int = 10) -> list[dict]:
        return [{"role": role, "value": count} for role, count in self.repository.top_roles(filters, limit)]

    def top_companies(self, filters: dict, limit: int = 10) -> list[dict]:
        return [{"company": company, "activity_score": count} for company, count in self.repository.top_companies(filters, limit)]

    def location_demand(self, filters: dict, by: str = "country", limit: int = 10) -> list[dict]:
        return [{"location": location, "value": count} for location, count in self.repository.top_locations(filters, by, limit)]

    def salary_overview(self, filters: dict, limit: int = 10) -> list[dict]:
        items = []
        for role, minimum, maximum, currency in self.repository.salary_by_role(filters, limit):
            items.append(
                {
                    "role": role,
                    "salary_range": SalaryRange(min=round(minimum, 2), max=round(maximum, 2), currency=currency).model_dump(),
                }
            )
        return items

    def industry_insights(self, filters: dict, limit: int = 15) -> list[dict]:
        return [{"industry": industry, "value": count} for industry, count in self.repository.top_industries(filters, limit)]

    def role_overview(self, role: str) -> RoleOverviewResponse:
        jobs = self.repository.jobs_for_role(role)
        skill_items = self.repository.top_skills_for_role(role)
        salary_items = self.repository.salary_by_role({"role": role}, limit=1)
        experience_items = self.repository.experience_distribution_for_role(role)
        remote_items = self.repository.remote_distribution_for_role(role)
        demand = len(jobs)
        salary_range = SalaryRange()
        if salary_items:
            _, minimum, maximum, currency = salary_items[0]
            salary_range = SalaryRange(min=round(minimum, 2), max=round(maximum, 2), currency=currency)

        fallback_overview = f"{role} roles are concentrated around {top_label(skill_items, 'core business')} skills and current hiring demand."
        overview = self.gemini.generate_text(
            f"Summarize the role '{role}' in 20 words for a job market dashboard.",
            fallback=fallback_overview,
        )
        return RoleOverviewResponse(
            role=role,
            overview=overview,
            demand_level=demand_level(demand),
            salary_range=salary_range,
            top_industry=self.repository.top_industry_for_role(role),
            experience_summary=summarize_levels(experience_items),
            remote_summary=summarize_remote(remote_items),
        )

    def compare_roles(self, role_1: str, role_2: str) -> CompareRolesResponse:
        left = self._build_compare_panel(role_1)
        right = self._build_compare_panel(role_2)
        common_skills = sorted(set(left.top_skills).intersection(set(right.top_skills)))
        salary_comparison = [
            {"role": left.name, "value": left.salary_range.max or left.salary_range.min or 0},
            {"role": right.name, "value": right.salary_range.max or right.salary_range.min or 0},
        ]
        demand_comparison = [
            {"role": left.name, "value": self._role_demand_value(left.name)},
            {"role": right.name, "value": self._role_demand_value(right.name)},
        ]
        fallback = self._comparison_fallback(left, right)
        final_insight = self.gemini.generate_text(
            f"Compare {left.name} and {right.name} for a career dashboard in one short sentence.",
            fallback=fallback,
        )
        return CompareRolesResponse(
            role_1=left,
            role_2=right,
            common_skills=common_skills,
            demand_comparison=demand_comparison,
            salary_comparison=salary_comparison,
            final_insight=final_insight,
        )

    def _role_demand_value(self, role: str) -> int:
        items = self.repository.top_roles({"role": role}, limit=1)
        return items[0][1] if items else 0

    def _build_compare_panel(self, role: str) -> CompareRolePanel:
        overview = self.role_overview(role)
        top_skills = [skill for skill, _ in self.repository.top_skills_for_role(role)]
        top_companies = [company for company, _ in self.repository.top_companies({"role": role}, limit=5)]
        experience_distribution = [
            {"level": level, "value": value} for level, value in self.repository.experience_distribution_for_role(role)
        ]
        summary = self.gemini.generate_text(
            f"Summarize the role '{role}' in 10 to 20 words for a career dashboard.",
            fallback=overview.overview,
        )
        return CompareRolePanel(
            name=role,
            summary=summary,
            demand_level=overview.demand_level,
            salary_range=overview.salary_range,
            top_industry=overview.top_industry,
            experience_summary=overview.experience_summary,
            remote_summary=overview.remote_summary,
            top_skills=top_skills,
            top_companies=top_companies,
            experience_distribution=experience_distribution,
        )

    def _comparison_fallback(self, left: CompareRolePanel, right: CompareRolePanel) -> str:
        left_salary = left.salary_range.max or left.salary_range.min or 0
        right_salary = right.salary_range.max or right.salary_range.min or 0
        if left_salary > right_salary:
            return f"{left.name} shows stronger salary upside, while {right.name} may be more accessible depending on skill overlap."
        if right_salary > left_salary:
            return f"{right.name} shows stronger salary upside, while {left.name} may be more accessible depending on skill overlap."
        return f"{left.name} and {right.name} show similar market positioning, with skill overlap likely shaping the better path."
