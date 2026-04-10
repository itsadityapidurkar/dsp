from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("job_id", name="uq_jobs_job_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_id: Mapped[str] = mapped_column(String(128), nullable=False)
    raw_job_title: Mapped[str | None] = mapped_column(String(255))
    job_title: Mapped[str | None] = mapped_column(String(255))
    normalized_job_title: Mapped[str | None] = mapped_column(String(255), index=True)
    company: Mapped[str | None] = mapped_column(String(255), index=True)
    location: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(128), index=True)
    country: Mapped[str | None] = mapped_column(String(128), index=True)
    employment_type: Mapped[str | None] = mapped_column(String(64))
    experience_level: Mapped[str | None] = mapped_column(String(64), index=True)
    salary_min: Mapped[float | None] = mapped_column(Float)
    salary_max: Mapped[float | None] = mapped_column(Float)
    salary_currency: Mapped[str | None] = mapped_column(String(16))
    job_description: Mapped[str | None] = mapped_column(Text)
    skills_raw: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(128), index=True)
    industry: Mapped[str | None] = mapped_column(String(128), index=True)
    remote_type: Mapped[str | None] = mapped_column(String(64))
    posted_date: Mapped[Date | None] = mapped_column(Date, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    skills: Mapped[list["JobSkill"]] = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")


class NormalizedSkill(Base):
    __tablename__ = "normalized_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    normalized_name: Mapped[str] = mapped_column(String(128), index=True)


class JobSkill(Base):
    __tablename__ = "job_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_pk: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    skill_name: Mapped[str] = mapped_column(String(128), index=True)

    job: Mapped[Job] = relationship("Job", back_populates="skills")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    extracted_text: Mapped[str] = mapped_column(Text)
    extracted_skills_json: Mapped[str] = mapped_column(Text)
    top_roles_json: Mapped[str] = mapped_column(Text)
    skill_gap_json: Mapped[str] = mapped_column(Text)
    match_score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
