from pydantic import BaseModel


class RankingItem(BaseModel):
    dimension_value: str
    current_value: float
    previous_value: float


class RankingData(BaseModel):
    metric: str
    current_period: str
    previous_period: str
    items: list[RankingItem]