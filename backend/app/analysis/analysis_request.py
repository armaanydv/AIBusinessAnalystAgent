from pydantic import BaseModel, Field, field_validator


class AnalysisRequest(BaseModel):
    metric: str | None = None
    dimensions: list[str] = Field(default_factory=list)
    filters: list[str] = Field(default_factory=list)
    time_period: str | None = None
    comparison: str | None = None
    objective: str | None = None
    analysis_type: str | None = None

    @field_validator("dimensions", "filters", mode="before")
    @classmethod
    def normalize_lists(cls, value):
        if value is None:
            return []

        return value

    def is_complete(self) -> bool:
        return len(self.missing_requirements()) == 0

    def missing_requirements(self) -> list[str]:
        missing = []

        if not self.metric:
            missing.append("metric")

        if not self.time_period:
            missing.append("time_period")

        if not self.objective:
            missing.append("objective")

        if not self.analysis_type:
            missing.append("analysis_type")

        # Comparative analysis specifically requires a comparison.
        if (
            self.analysis_type == "comparative"
            and not self.comparison
        ):
            missing.append("comparison")

        return missing