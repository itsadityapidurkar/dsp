from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.v1.deps import get_resume_service
from app.schemas.resume import ResumeAnalysisResponse, ResumeRecommendationsResponse, ResumeSkillGapResponse
from app.services.resume_service import ResumeService


router = APIRouter()


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...), service: ResumeService = Depends(get_resume_service)) -> dict:
    try:
        content = await file.read()
        return service.analyze_resume(file.filename or "resume", content).model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/recommendations", response_model=ResumeRecommendationsResponse)
async def recommendations(file: UploadFile = File(...), service: ResumeService = Depends(get_resume_service)) -> dict:
    try:
        content = await file.read()
        result = service.analyze_resume(file.filename or "resume", content)
        return {"items": [item.model_dump() for item in result.recommended_roles]}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/skill-gap", response_model=ResumeSkillGapResponse)
async def skill_gap(file: UploadFile = File(...), service: ResumeService = Depends(get_resume_service)) -> dict:
    try:
        content = await file.read()
        result = service.analyze_resume(file.filename or "resume", content)
        return {"your_skills": result.your_skills, "missing_skills": result.missing_skills}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
