from pydantic import BaseModel


class Contribution(BaseModel):
    contributor: str
    change: float
    contribution_percentage: float


class ContributionData(BaseModel):
    metric: str
    current_period: str
    previous_period: str
    total_change: float
    contributions: list[Contribution]