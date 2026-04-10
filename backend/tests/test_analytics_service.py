from app.services.analytics_service import AnalyticsService


class StubRepository:
    def top_skills(self, filters, limit=15):
        return [("Python", 10), ("SQL", 8)]

    def top_categories(self, filters, limit=10):
        return [("Data & AI", 10)]

    def top_roles(self, filters, limit=10):
        if filters.get("role"):
            return [(filters["role"], 1200)]
        return [("Data Analyst", 1200), ("Backend Engineer", 900)]

    def top_companies(self, filters, limit=10):
        return [("Acme", 25), ("Globex", 20)]

    def top_locations(self, filters, by="country", limit=10):
        return [("India", 20), ("United States", 10)]

    def salary_by_role(self, filters, limit=10):
        role = filters.get("role", "Data Analyst")
        return [(role, 60000.0, 90000.0, "USD")]

    def jobs_for_role(self, role):
        return [object()] * 1200

    def top_industry_for_role(self, role):
        return "Technology"

    def experience_distribution_for_role(self, role):
        return [("Entry", 40), ("Mid", 30)]

    def remote_distribution_for_role(self, role):
        return [("Hybrid", 50), ("On-site", 30)]

    def top_skills_for_role(self, role, limit=10):
        return [("Python", 10), ("SQL", 8), ("Power BI", 5)]

    def list_roles(self):
        return ["Data Analyst", "Backend Engineer"]


class StubGemini:
    def generate_text(self, prompt: str, fallback: str) -> str:
        return fallback


def test_role_overview_has_expected_shape():
    service = AnalyticsService(StubRepository(), StubGemini())
    result = service.role_overview("Data Analyst")
    assert result.role == "Data Analyst"
    assert result.demand_level == "High"
    assert result.salary_range.currency == "USD"


def test_compare_roles_returns_common_skills():
    service = AnalyticsService(StubRepository(), StubGemini())
    result = service.compare_roles("Data Analyst", "Backend Engineer")
    assert "Python" in result.common_skills
    assert len(result.demand_comparison) == 2
