from fastapi import APIRouter, Depends

from app.api.v1.deps import get_analytics_service, get_repository
from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import (
    CompanyBreakdownResponse,
    ExperienceBreakdownResponse,
    LocationDemandResponse,
    RoleOverviewResponse,
    SalaryOverviewResponse,
    SkillBreakdownResponse,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("")
def list_roles(repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return {"items": repository.list_roles()}


@router.get("/{role_name}/overview", response_model=RoleOverviewResponse)
def overview(role_name: str, service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return service.role_overview(role_name).model_dump()


@router.get("/{role_name}/skills", response_model=SkillBreakdownResponse)
def skills(role_name: str, repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return {"items": [{"skill": skill, "value": value} for skill, value in repository.top_skills_for_role(role_name)]}


@router.get("/{role_name}/companies", response_model=CompanyBreakdownResponse)
def companies(role_name: str, repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return {"items": [{"company": company, "value": value} for company, value in repository.top_companies({"role": role_name})]}


@router.get("/{role_name}/salary", response_model=SalaryOverviewResponse)
def salary(role_name: str, service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    items = service.salary_overview({"role": role_name}, limit=1)
    return {"items": items}


@router.get("/{role_name}/locations", response_model=LocationDemandResponse)
def locations(role_name: str, repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return {"items": [{"location": name, "value": value} for name, value in repository.top_locations({"role": role_name})]}


@router.get("/{role_name}/experience", response_model=ExperienceBreakdownResponse)
def experience(role_name: str, repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return {"items": [{"level": level, "value": value} for level, value in repository.experience_distribution_for_role(role_name)]}
