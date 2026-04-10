from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

DEFAULT_CSV = Path("/mnt/g/DSPPR/DataSets/outputs/unified_jobs_dataset.csv")
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from data_pipeline.clean_and_normalize import standardize_frame
from data_pipeline.skill_normalization import parse_skills


def csv_chunks(csv_path: Path, chunk_size: int):
    return pd.read_csv(
        csv_path,
        chunksize=chunk_size,
        low_memory=False,
        dtype={"job_id": "string"},
    )


def clean_value(value):
    if value is None:
        return None
    if isinstance(value, (list, dict, tuple, set)):
        return value
    if isinstance(value, float) and math.isnan(value):
        return None
    if pd.isna(value):
        return None
    return value


def load_to_database(
    csv_path: Path,
    database_url: str,
    truncate: bool = False,
    chunk_size: int = 5000,
    limit: int | None = None,
) -> None:
    from app.db.session import Base
    from app.models.job import Job, JobSkill

    engine = create_engine(database_url, future=True)
    Base.metadata.create_all(engine)
    processed = 0
    seen_job_ids: set[str] = set()

    with Session(engine) as session:
        if truncate:
            session.execute(delete(JobSkill))
            session.execute(delete(Job))
            session.commit()

        for chunk in csv_chunks(csv_path, chunk_size):
            frame = standardize_frame(chunk)
            for row in frame.to_dict(orient="records"):
                row = {key: clean_value(value) for key, value in row.items()}
                if limit is not None and processed >= limit:
                    session.commit()
                    return

                job_id = str(row["job_id"]).strip()
                if not job_id or job_id.lower() == "none":
                    continue
                if job_id in seen_job_ids:
                    continue
                seen_job_ids.add(job_id)

                existing_job_id = session.scalar(select(Job.id).where(Job.job_id == job_id))
                if existing_job_id is not None:
                    session.execute(delete(JobSkill).where(JobSkill.job_pk == existing_job_id))

                merged_job = session.merge(
                    Job(
                        job_id=job_id,
                        raw_job_title=row.get("raw_job_title"),
                        job_title=row.get("job_title"),
                        normalized_job_title=row.get("normalized_job_title"),
                        company=row.get("company"),
                        location=row.get("location"),
                        city=row.get("city"),
                        country=row.get("country"),
                        employment_type=row.get("employment_type"),
                        experience_level=row.get("experience_level"),
                        salary_min=row.get("salary_min"),
                        salary_max=row.get("salary_max"),
                        salary_currency=row.get("salary_currency"),
                        job_description=row.get("job_description"),
                        skills_raw=json.dumps(row.get("skills", [])),
                        category=row.get("category"),
                        industry=row.get("industry"),
                        remote_type=row.get("remote_type"),
                        posted_date=row.get("posted_date"),
                    )
                )
                session.flush()
                for skill in parse_skills(row.get("skills")):
                    session.add(JobSkill(job_pk=merged_job.id, skill_name=skill))
                processed += 1

            session.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Load unified job market data into the database.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--truncate", action="store_true")
    parser.add_argument("--chunk-size", type=int, default=5000)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    load_to_database(
        Path(args.csv),
        args.database_url,
        truncate=args.truncate,
        chunk_size=args.chunk_size,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
