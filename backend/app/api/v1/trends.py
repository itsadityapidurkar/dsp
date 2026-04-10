from fastapi import APIRouter, Depends, Query

from app.api.v1.dashboard import filters_dependency
from app.api.v1.deps import get_analytics_service
from app.schemas.analytics import (
    CompanyActivityResponse,
    IndustryInsightResponse,
    LocationDemandResponse,
    RoleDemandResponse,
    SalaryOverviewResponse,
    SkillDemandResponse,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/skills", response_model=SkillDemandResponse)
def skills(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_skills(filters)}


@router.get("/roles", response_model=RoleDemandResponse)
def roles(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_roles(filters, limit=20)}


@router.get("/companies", response_model=CompanyActivityResponse)
def companies(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.top_companies(filters, limit=20)}


@router.get("/locations", response_model=LocationDemandResponse)
def locations(
    by: str = Query(default="country", pattern="^(country|city)$"),
    filters: dict = Depends(filters_dependency),
    service: AnalyticsService = Depends(get_analytics_service),
) -> dict:
    return {"items": service.location_demand(filters, by=by, limit=20)}


@router.get("/salaries", response_model=SalaryOverviewResponse)
def salaries(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.salary_overview(filters, limit=20)}


@router.get("/industries", response_model=IndustryInsightResponse)
def industries(filters: dict = Depends(filters_dependency), service: AnalyticsService = Depends(get_analytics_service)) -> dict:
    return {"items": service.industry_insights(filters)}
