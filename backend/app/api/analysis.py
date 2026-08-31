from fastapi import APIRouter

from app.api.schemas.analysis import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
)
from app.core.bootstrap import analysis_service


router = APIRouter()


@router.post(
    "/analysis",
    response_model=AnalysisResponseSchema,
)
def analyze(
    request: AnalysisRequestSchema,
):
    result = analysis_service.analyze(
        request.query
    )

    return AnalysisResponseSchema(
        analysis_type=result.analysis_type,
        findings=result.findings,
        conclusions=result.conclusions,
        supporting_evidence=result.supporting_evidence,
    )