from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    metric: str | None = None
    dimensions: list[str] = Field(default_factory=list)
    filters: list[str] = Field(default_factory=list)
    time_period: str | None = None
    comparison: str | None = None
    objective: str | None = None
    analysis_type: str | None = None

    def is_complete(self) -> bool:
        return len(self.missing_requirements()) == 0

    def missing_requirements(self) -> list[str]:
        missing = []

        if not self.metric:
            missing.append("metric")

        if not self.time_period:
            missing.append("time_period")

        if not self.comparison:
            missing.append("comparison")

        if not self.analysis_type:
            missing.append("analysis_type")

        return missing