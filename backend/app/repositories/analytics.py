from __future__ import annotations

from collections import Counter
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job, JobSkill


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_roles(self) -> list[str]:
        stmt = select(Job.normalized_job_title).where(Job.normalized_job_title.is_not(None)).distinct().order_by(Job.normalized_job_title.asc())
        return [item for item in self.db.scalars(stmt).all() if item]

    def filtered_jobs_query(self, filters: dict):
        stmt = select(Job)
        if filters.get("category"):
            stmt = stmt.where(Job.category == filters["category"])
        if filters.get("role"):
            stmt = stmt.where(Job.normalized_job_title == filters["role"])
        if filters.get("country"):
            stmt = stmt.where(Job.country == filters["country"])
        if filters.get("city"):
            stmt = stmt.where(Job.city == filters["city"])
        if filters.get("industry"):
            stmt = stmt.where(Job.industry == filters["industry"])
        if filters.get("experience_level"):
            stmt = stmt.where(Job.experience_level == filters["experience_level"])
        if filters.get("remote_type"):
            stmt = stmt.where(Job.remote_type == filters["remote_type"])
        return stmt

    def top_categories(self, filters: dict, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(Job.category, func.count(Job.id))
            .where(Job.category.is_not(None))
            .group_by(Job.category)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, count) for name, count in self.db.execute(stmt).all() if name]

    def top_industries(self, filters: dict, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(Job.industry, func.count(Job.id))
            .where(Job.industry.is_not(None))
            .group_by(Job.industry)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, count) for name, count in self.db.execute(stmt).all() if name]

    def top_roles(self, filters: dict, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(Job.normalized_job_title, func.count(Job.id))
            .where(Job.normalized_job_title.is_not(None))
            .group_by(Job.normalized_job_title)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, count) for name, count in self.db.execute(stmt).all() if name]

    def top_companies(self, filters: dict, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(Job.company, func.count(Job.id))
            .where(Job.company.is_not(None))
            .group_by(Job.company)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, count) for name, count in self.db.execute(stmt).all() if name and name != "Unknown"]

    def top_locations(self, filters: dict, by: str = "country", limit: int = 10) -> list[tuple[str, int]]:
        column = Job.city if by == "city" else Job.country
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(column, func.count(Job.id))
            .where(column.is_not(None))
            .group_by(column)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, count) for name, count in self.db.execute(stmt).all() if name]

    def salary_by_role(self, filters: dict, limit: int = 10) -> list[tuple[str, float, float, str | None]]:
        stmt = (
            self.filtered_jobs_query(filters)
            .with_only_columns(
                Job.normalized_job_title,
                func.avg(Job.salary_min),
                func.avg(Job.salary_max),
                func.max(Job.salary_currency),
            )
            .where(Job.salary_min.is_not(None), Job.salary_max.is_not(None), Job.normalized_job_title.is_not(None))
            .group_by(Job.normalized_job_title)
            .order_by(func.count(Job.id).desc())
            .limit(limit)
        )
        return [(name, float(minimum), float(maximum), currency) for name, minimum, maximum, currency in self.db.execute(stmt).all() if name]

    def experience_distribution_for_role(self, role: str) -> list[tuple[str, int]]:
        stmt = (
            select(Job.experience_level, func.count(Job.id))
            .where(Job.normalized_job_title == role, Job.experience_level.is_not(None))
            .group_by(Job.experience_level)
            .order_by(func.count(Job.id).desc())
        )
        return [(level, count) for level, count in self.db.execute(stmt).all() if level]

    def top_industry_for_role(self, role: str) -> str:
        stmt = (
            select(Job.industry, func.count(Job.id))
            .where(Job.normalized_job_title == role, Job.industry.is_not(None))
            .group_by(Job.industry)
            .order_by(func.count(Job.id).desc())
            .limit(1)
        )
        row = self.db.execute(stmt).first()
        return row[0] if row else "Unknown"

    def remote_distribution_for_role(self, role: str) -> list[tuple[str, int]]:
        stmt = (
            select(Job.remote_type, func.count(Job.id))
            .where(Job.normalized_job_title == role, Job.remote_type.is_not(None))
            .group_by(Job.remote_type)
            .order_by(func.count(Job.id).desc())
        )
        return [(remote_type, count) for remote_type, count in self.db.execute(stmt).all() if remote_type]

    def top_skills(self, filters: dict, limit: int = 15) -> list[tuple[str, int]]:
        job_ids_subquery = self.filtered_jobs_query(filters).with_only_columns(Job.id).subquery()
        stmt = (
            select(JobSkill.skill_name, func.count(JobSkill.id))
            .where(JobSkill.job_pk.in_(select(job_ids_subquery.c.id)))
            .group_by(JobSkill.skill_name)
            .order_by(func.count(JobSkill.id).desc())
            .limit(limit)
        )
        return [(skill, count) for skill, count in self.db.execute(stmt).all() if skill]

    def top_skills_for_role(self, role: str, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            select(JobSkill.skill_name, func.count(JobSkill.id))
            .join(Job, Job.id == JobSkill.job_pk)
            .where(Job.normalized_job_title == role)
            .group_by(JobSkill.skill_name)
            .order_by(func.count(JobSkill.id).desc())
            .limit(limit)
        )
        return [(skill, count) for skill, count in self.db.execute(stmt).all() if skill]

    def jobs_for_role(self, role: str) -> list[Job]:
        stmt = select(Job).where(Job.normalized_job_title == role)
        return self.db.scalars(stmt).all()

    def filter_metadata(self) -> dict[str, list[str]]:
        def values(column) -> list[str]:
            stmt = select(column).where(column.is_not(None)).distinct().order_by(column.asc())
            return [item for item in self.db.scalars(stmt).all() if item]

        return {
            "categories": values(Job.category),
            "roles": values(Job.normalized_job_title),
            "countries": values(Job.country),
            "cities": values(Job.city),
            "industries": values(Job.industry),
            "experience_levels": values(Job.experience_level),
            "remote_types": values(Job.remote_type),
        }
