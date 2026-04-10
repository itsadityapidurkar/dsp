import ast
from typing import Iterable


ALIASES = {
    "js": "JavaScript",
    "py": "Python",
    "power bi": "Power BI",
    "postgres": "PostgreSQL",
}


def normalize_skill(skill: str) -> str:
    cleaned = " ".join((skill or "").strip().split())
    if not cleaned:
        return ""
    lowered = cleaned.lower()
    return ALIASES.get(lowered, cleaned)


def parse_skills(raw: str | None) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        return [normalize_skill(str(item)) for item in raw if normalize_skill(str(item))]
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return [normalize_skill(str(item)) for item in parsed if normalize_skill(str(item))]
    except Exception:
        pass
    parts = [part.strip() for part in str(raw).replace("|", ",").split(",")]
    return [normalize_skill(part) for part in parts if normalize_skill(part)]
