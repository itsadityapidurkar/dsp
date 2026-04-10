from pydantic import BaseModel


class SimpleMetric(BaseModel):
    label: str
    value: int


class SalaryRange(BaseModel):
    min: float | None = None
    max: float | None = None
    currency: str | None = None
