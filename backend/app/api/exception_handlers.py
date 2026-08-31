import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.ingestion_exceptions import IngestionError
from app.exceptions.llm_exceptions import LLMError
from app.exceptions.output_validation_exception import (
    OutputValidationException,
)


async def llm_exception_handler(
    request: Request,
    exc: LLMError,
):
    """
    Handle LLM-related errors.
    """

    traceback.print_exc()

    return JSONResponse(
        status_code=502,
        content={
            "detail": str(exc),
        },
    )


async def ingestion_exception_handler(
    request: Request,
    exc: IngestionError,
):
    """
    Handle document ingestion errors.
    """

    traceback.print_exc()

    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
        },
    )


async def output_validation_exception_handler(
    request: Request,
    exc: OutputValidationException,
):
    """
    Handle invalid LLM output.
    """

    traceback.print_exc()

    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
        },
    )


async def value_error_handler(
    request: Request,
    exc: ValueError,
):
    """
    Handle invalid request or analysis input.
    """

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected errors.
    """

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
        },
    )