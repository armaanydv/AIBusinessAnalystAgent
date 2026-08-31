from pathlib import Path
import os
import tempfile
import traceback

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.schemas.upload import UploadResponseSchema
from app.core.bootstrap import ingestion_service
from app.exceptions.ingestion_exceptions import (
    EmptyDocumentError,
)
from app.validators.upload_validator import validate_upload


router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponseSchema,
)
async def upload_pdf(
    file: UploadFile = File(...),
):
    temp_path = None

    try:
        # ---------------------------------------------------------
        # Read uploaded file
        # ---------------------------------------------------------

        content = await file.read()

        # ---------------------------------------------------------
        # Validate upload
        # ---------------------------------------------------------

        validate_upload(
            filename=file.filename,
            content=content,
        )

        # ---------------------------------------------------------
        # Save uploaded file temporarily
        # ---------------------------------------------------------

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(content)

            temp_path = temp_file.name

        # ---------------------------------------------------------
        # Run ingestion pipeline
        # ---------------------------------------------------------

        document, chunks = ingestion_service.ingest(
            temp_path
        )

        # ---------------------------------------------------------
        # Success response
        # ---------------------------------------------------------

        return UploadResponseSchema(
            message="Document ingested successfully.",
            document_id=document.metadata.document_id,
            pages=len(document.pages),
            chunks_created=len(chunks.chunks),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except EmptyDocumentError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except HTTPException:
        raise

    except Exception as exc:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "during document ingestion."
            ),
        ) from exc

    finally:
        if (
            temp_path is not None
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)