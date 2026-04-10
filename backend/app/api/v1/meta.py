from fastapi import APIRouter, Depends

from app.api.v1.deps import get_repository
from app.repositories.analytics import AnalyticsRepository


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/meta/filters")
def filters(repository: AnalyticsRepository = Depends(get_repository)) -> dict:
    return repository.filter_metadata()
