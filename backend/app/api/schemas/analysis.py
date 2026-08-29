from pydantic import BaseModel, Field


class AnalysisRequestSchema(BaseModel):
    """
    Request body for the business analysis API.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Business question to analyze.",
    )


class AnalysisResponseSchema(BaseModel):
    """
    Response returned by the business analysis API.
    """

    analysis_type: str

    findings: list[str]

    conclusions: list[str]

    supporting_evidence: list[str]