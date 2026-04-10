from pydantic import BaseModel

from app.schemas.common import SalaryRange


class DashboardItem(BaseModel):
    label: str
    demand_score: int


class CategoryDistributionItem(BaseModel):
    category: str
    value: int


class CompanyActivityItem(BaseModel):
    company: str
    activity_score: int


class LocationDemandItem(BaseModel):
    location: str
    value: int


class SalaryOverviewItem(BaseModel):
    role: str
    salary_range: SalaryRange


class NamedItemsResponse(BaseModel):
    items: list[dict]


class SkillDemandItem(BaseModel):
    skill: str
    demand_score: int


class SkillDemandResponse(BaseModel):
    items: list[SkillDemandItem]


class CategoryDistributionResponse(BaseModel):
    items: list[CategoryDistributionItem]


class RoleDemandItem(BaseModel):
    role: str
    value: int


class RoleDemandResponse(BaseModel):
    items: list[RoleDemandItem]


class CompanyActivityResponse(BaseModel):
    items: list[CompanyActivityItem]


class LocationDemandResponse(BaseModel):
    items: list[LocationDemandItem]


class SalaryOverviewResponse(BaseModel):
    items: list[SalaryOverviewItem]


class SkillBreakdownItem(BaseModel):
    skill: str
    value: int


class SkillBreakdownResponse(BaseModel):
    items: list[SkillBreakdownItem]


class CompanyBreakdownItem(BaseModel):
    company: str
    value: int


class CompanyBreakdownResponse(BaseModel):
    items: list[CompanyBreakdownItem]


class ExperienceBreakdownItem(BaseModel):
    level: str
    value: int


class ExperienceBreakdownResponse(BaseModel):
    items: list[ExperienceBreakdownItem]


class IndustryInsightItem(BaseModel):
    industry: str
    value: int


class IndustryInsightResponse(BaseModel):
    items: list[IndustryInsightItem]


class FiltersResponse(BaseModel):
    categories: list[str]
    roles: list[str]
    countries: list[str]
    cities: list[str]
    industries: list[str]
    experience_levels: list[str]
    remote_types: list[str]


class RoleOverviewResponse(BaseModel):
    role: str
    overview: str
    demand_level: str
    salary_range: SalaryRange
    top_industry: str
    experience_summary: str
    remote_summary: str


class CompareRolePanel(BaseModel):
    name: str
    summary: str
    demand_level: str
    salary_range: SalaryRange
    top_industry: str
    experience_summary: str
    remote_summary: str
    top_skills: list[str]
    top_companies: list[str]
    experience_distribution: list[dict]


class CompareRolesResponse(BaseModel):
    role_1: CompareRolePanel
    role_2: CompareRolePanel
    common_skills: list[str]
    demand_comparison: list[dict]
    salary_comparison: list[dict]
    final_insight: str
