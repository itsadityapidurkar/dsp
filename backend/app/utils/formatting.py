from collections import Counter


EXPERIENCE_ORDER = {"Intern": 0, "Entry": 1, "Mid": 2, "Senior": 3, "Lead": 4}


def demand_level(count: int) -> str:
    if count >= 5000:
        return "Very High"
    if count >= 1000:
        return "High"
    if count >= 250:
        return "Moderate"
    return "Emerging"


def summarize_levels(items: list[tuple[str, int]]) -> str:
    if not items:
        return "Not enough market information"
    ordered = sorted(items, key=lambda item: EXPERIENCE_ORDER.get(item[0], 99))
    labels = [label for label, _ in ordered[:2]]
    return " to ".join(labels)


def summarize_remote(items: list[tuple[str, int]]) -> str:
    if not items:
        return "Limited remote availability data"
    label, _ = max(items, key=lambda item: item[1])
    if label == "Remote":
        return "Strong remote availability"
    if label == "Hybrid":
        return "Balanced hybrid availability"
    return "Primarily on-site"


def top_label(items: list[tuple[str, int]], fallback: str = "Unknown") -> str:
    return items[0][0] if items else fallback
