from pydantic import BaseModel


class ComparisonData(BaseModel):
    """
    Structured numerical data extracted from retrieved evidence
    for comparative analysis.
    """

    metric: str

    current_value: float

    previous_value: float

    current_period: str

    previous_period: str

    dimension: str | None = None

    dimension_value: str | None = None