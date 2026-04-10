from __future__ import annotations

import pandas as pd

from data_pipeline.skill_normalization import parse_skills


def standardize_frame(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    frame.columns = [column.strip() for column in frame.columns]
    frame = frame.replace({"": None, "nan": None, "NaN": None})
    for text_column in ["job_title", "normalized_job_title", "company", "location", "city", "country", "category", "industry", "remote_type"]:
        if text_column in frame.columns:
            frame[text_column] = frame[text_column].astype("string").str.strip()
    if "posted_date" in frame.columns:
        frame["posted_date"] = pd.to_datetime(frame["posted_date"], errors="coerce", dayfirst=True).dt.date
    if "skills" in frame.columns:
        frame["skills"] = frame["skills"].apply(parse_skills)
    for salary_column in ["salary_min", "salary_max"]:
        if salary_column in frame.columns:
            frame[salary_column] = pd.to_numeric(frame[salary_column], errors="coerce")
    return frame.where(pd.notnull(frame), None)
