from pydantic import BaseModel


class TrendData(BaseModel):
    metric: str
    periods: list[str]
    values: list[float]
    dimension: str | None = None
    dimension_value: str | None = None