import asyncio

from app.api.v1.compare import compare_roles
from app.api.v1.dashboard import top_skills
from app.api.v1.resume import recommendations
from app.main import app


class StubAnalyticsService:
    def top_skills(self, filters):
        return [{"skill": "Python", "demand_score": 10}]

    def category_distribution(self, filters):
        return [{"category": "Data & AI", "value": 12}]

    def top_roles(self, filters, limit=10):
        return [{"role": "Data Analyst", "value": 8}]

    def top_companies(self, filters, limit=10):
        return [{"company": "Acme", "activity_score": 7}]

    def location_demand(self, filters, by="country", limit=10):
        return [{"location": "India", "value": 5}]

    def salary_overview(self, filters, limit=10):
        return [{"role": "Data Analyst", "salary_range": {"min": 50000, "max": 80000, "currency": "USD"}}]

    def industry_insights(self, filters, limit=15):
        return [{"industry": "Technology", "value": 6}]

    def role_overview(self, role):
        return type(
            "Overview",
            (),
            {
                "model_dump": lambda self: {
                    "role": role,
                    "overview": "Analytics-focused role supporting business decisions.",
                    "demand_level": "High",
                    "salary_range": {"min": 50000, "max": 80000, "currency": "USD"},
                    "top_industry": "Technology",
                    "experience_summary": "Entry to Mid",
                    "remote_summary": "Balanced hybrid availability",
                }
            },
        )()

    def compare_roles(self, role1, role2):
        return type(
            "Comparison",
            (),
            {
                "model_dump": lambda self: {
                    "role_1": {
                        "name": role1,
                        "summary": "Role one summary",
                        "demand_level": "High",
                        "salary_range": {"min": 1, "max": 2, "currency": "USD"},
                        "top_industry": "Tech",
                        "experience_summary": "Entry",
                        "remote_summary": "Hybrid",
                        "top_skills": ["Python"],
                        "top_companies": ["Acme"],
                        "experience_distribution": [{"level": "Entry", "value": 1}],
                    },
                    "role_2": {
                        "name": role2,
                        "summary": "Role two summary",
                        "demand_level": "Moderate",
                        "salary_range": {"min": 2, "max": 3, "currency": "USD"},
                        "top_industry": "Finance",
                        "experience_summary": "Mid",
                        "remote_summary": "On-site",
                        "top_skills": ["SQL"],
                        "top_companies": ["Globex"],
                        "experience_distribution": [{"level": "Mid", "value": 1}],
                    },
                    "common_skills": [],
                    "demand_comparison": [{"role": role1, "value": 1}, {"role": role2, "value": 2}],
                    "salary_comparison": [{"role": role1, "value": 2}, {"role": role2, "value": 3}],
                    "final_insight": "Comparison insight",
                }
            },
        )()


class StubRepository:
    def list_roles(self):
        return ["Data Analyst", "Backend Engineer"]

    def top_skills_for_role(self, role):
        return [("Python", 10)]

    def top_companies(self, filters):
        return [("Acme", 7)]

    def top_locations(self, filters):
        return [("India", 5)]

    def experience_distribution_for_role(self, role):
        return [("Entry", 3)]


class StubResumeService:
    def analyze_resume(self, filename, content):
        return type(
            "ResumeResult",
            (),
            {
                "model_dump": lambda self: {
                    "match_score": 75,
                    "recommended_roles": [{"role": "Data Analyst", "score": 75}],
                    "your_skills": ["Python"],
                    "missing_skills": ["SQL"],
                    "suggestions": ["Build SQL depth."],
                    "learning_resources": [{"skill": "SQL", "title": "SQL Tutorial", "url": "https://example.com"}],
                    "insight": "Strong analytics base.",
                    "profile_summary": "Strong early analytics profile.",
                },
                "recommended_roles": [type("Role", (), {"model_dump": lambda self: {"role": "Data Analyst", "score": 75}})()],
                "your_skills": ["Python"],
                "missing_skills": ["SQL"],
            },
        )()


def test_health_route_is_registered():
    paths = {route.path for route in app.router.routes}
    assert "/api/v1/health" in paths


def test_dashboard_skills_endpoint():
    response = top_skills(filters={}, service=StubAnalyticsService())
    assert response["items"][0]["skill"] == "Python"


def test_compare_roles_endpoint():
    response = compare_roles(role1="Data Analyst", role2="Backend Engineer", service=StubAnalyticsService())
    assert response["role_1"]["name"] == "Data Analyst"


def test_resume_recommendations_endpoint():
    class UploadStub:
        filename = "resume.pdf"

        async def read(self):
            return b"python sql"

    response = asyncio.run(recommendations(file=UploadStub(), service=StubResumeService()))
    assert response["items"][0]["role"] == "Data Analyst"
