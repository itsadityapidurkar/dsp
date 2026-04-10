from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.analytics import AnalyticsRepository
from app.services.analytics_service import AnalyticsService
from app.services.gemini_service import GeminiService
from app.services.resume_service import ResumeService


def get_repository(db: Session = Depends(get_db)) -> AnalyticsRepository:
    return AnalyticsRepository(db)


def get_analytics_service(repository: AnalyticsRepository = Depends(get_repository)) -> AnalyticsService:
    return AnalyticsService(repository, GeminiService())


def get_resume_service(repository: AnalyticsRepository = Depends(get_repository)) -> ResumeService:
    return ResumeService(repository, GeminiService())
