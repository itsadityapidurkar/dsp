from pydantic import BaseModel


class RecommendedRole(BaseModel):
    role: str
    score: int


class LearningResource(BaseModel):
    skill: str
    title: str
    url: str


class ResumeAnalysisResponse(BaseModel):
    match_score: int
    recommended_roles: list[RecommendedRole]
    your_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    learning_resources: list[LearningResource]
    insight: str
    profile_summary: str


class ResumeRecommendationsResponse(BaseModel):
    items: list[RecommendedRole]


class ResumeSkillGapResponse(BaseModel):
    your_skills: list[str]
    missing_skills: list[str]
