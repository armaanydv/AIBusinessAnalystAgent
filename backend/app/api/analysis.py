import traceback

from fastapi import APIRouter, HTTPException

from app.core.bootstrap import analysis_service

router = APIRouter()


@router.post("/analysis")
def analyze(query: str):
    try:
        result = analysis_service.analyze(query)

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc