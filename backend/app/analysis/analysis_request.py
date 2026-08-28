from pydantic import BaseModel, Field


ANALYSIS_REQUIREMENTS = {
    "comparative": {
        "metric": True,
        "time_period": True,
        "comparison": True,
        "objective": True,
    },
    "trend": {
        "metric": True,
        "time_period": True,
        "comparison": False,
        "objective": True,
    },
    "ranking": {
        "metric": True,
        "time_period": True,
        "comparison": False,
        "objective": True,
    },
    "root_cause": {
        "metric": True,
        "time_period": True,
        "comparison": False,
        "objective": True,
    },
    "contribution": {
        "metric": True,
        "time_period": True,
        "comparison": False,
        "objective": True,
    },
    "swot": {
        "metric": False,
        "time_period": False,
        "comparison": False,
        "objective": True,
    },
}


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

        # Analysis type itself must be identified.
        if not self.analysis_type:
            missing.append("analysis_type")
            return missing

        # The analysis type must be supported.
        requirements = ANALYSIS_REQUIREMENTS.get(
            self.analysis_type
        )

        if requirements is None:
            missing.append("analysis_type")
            return missing

        # Validate the requirements declared for the
        # selected analysis technique.
        if requirements["metric"] and not self.metric:
            missing.append("metric")

        if (
            requirements["time_period"]
            and not self.time_period
        ):
            missing.append("time_period")

        if (
            requirements["comparison"]
            and not self.comparison
        ):
            missing.append("comparison")

        if requirements["objective"] and not self.objective:
            missing.append("objective")

        return missing