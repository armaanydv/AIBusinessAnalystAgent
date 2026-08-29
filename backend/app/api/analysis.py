import traceback

from fastapi import APIRouter, HTTPException

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
    try:
        result = analysis_service.analyze(
            request.query
        )

        return AnalysisResponseSchema(
            analysis_type=result.analysis_type,
            findings=result.findings,
            conclusions=result.conclusions,
            supporting_evidence=result.supporting_evidence,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc