from pathlib import Path
import os
import tempfile
import traceback

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.bootstrap import ingestion_service
from app.validators.upload_validator import validate_upload

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
):
    # ---------------------------------------------------------
    # Validate upload
    # ---------------------------------------------------------

    if not validate_upload():
        raise HTTPException(
            status_code=400,
            detail="Upload validation failed.",
        )

    temp_path = None

    try:
        # ---------------------------------------------------------
        # Save uploaded file temporarily
        # ---------------------------------------------------------

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            content = await file.read()
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

        return {
            "message": "Document ingested successfully.",
            "document_id": document.metadata.document_id,
            "pages": len(document.pages),
            "chunks_created": len(chunks.chunks),
        }

    except Exception:
        traceback.print_exc()
        raise

    finally:
        if (
            temp_path is not None
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)