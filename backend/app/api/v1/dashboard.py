from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_analytics_service
from app.schemas.analytics import (
    CategoryDistributionResponse,
    CompanyActivityResponse,
    LocationDemandResponse,
    RoleDemandResponse,
    SalaryOverviewResponse,
    SkillDemandResponse,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter()


def filters_dependency(
    category: str | None = None,
    role: str | None = None,
    country: str | None = None,
    city: str | None = None,
    industry: str | None = None,
    experience_level: str | None = None,
    remote_type: str | None = None,
) -> dict:
    return {
        "category": category,
        "role": role,
        "country": country,
        "city": city,
        "industry": industry,
        "experience_level": experience_level,
        "remote_type": remote_type,
    }


@router.get("/skills/top", response_model=SkillDemandResponse)
def top_skills(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_skills(filters)}


@router.get("/categories/distribution", response_model=CategoryDistributionResponse)
def categories(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.category_distribution(filters)}


@router.get("/roles/top", response_model=RoleDemandResponse)
def roles(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_roles(filters)}


@router.get("/companies/top", response_model=CompanyActivityResponse)
def companies(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_companies(filters)}


@router.get("/locations/demand", response_model=LocationDemandResponse)
def locations(
    by: str = Query(default="country", pattern="^(country|city)$"),
    filters: dict = Depends(filters_dependency),
    service: AnalyticsService = Depends(get_analytics_service),
) -> dict:
    return {"items": service.location_demand(filters, by=by)}


@router.get("/salary/overview", response_model=SalaryOverviewResponse)
def salary(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.salary_overview(filters)}
