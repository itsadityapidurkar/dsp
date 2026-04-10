from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_analytics_service
from app.schemas.analytics import CompareRolesResponse
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/roles", response_model=CompareRolesResponse)
def compare_roles(
    role1: str = Query(..., min_length=1),
    role2: str = Query(..., min_length=1),
    service: AnalyticsService = Depends(get_analytics_service),
) -> dict:
    return service.compare_roles(role1, role2).model_dump()
