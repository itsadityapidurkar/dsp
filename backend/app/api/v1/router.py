from fastapi import APIRouter

from app.api.v1 import compare, dashboard, meta, resume, roles, trends


api_router = APIRouter()
api_router.include_router(meta.router, tags=["meta"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(compare.router, prefix="/compare", tags=["compare"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
