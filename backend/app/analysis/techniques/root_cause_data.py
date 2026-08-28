from pydantic import BaseModel


class RootCause(BaseModel):
    cause: str
    evidence: str
    impact: str


class RootCauseData(BaseModel):
    metric: str
    current_period: str
    previous_period: str
    current_value: float
    previous_value: float
    causes: list[RootCause]