from pathlib import Path
import os
import tempfile

from fastapi import APIRouter, File, UploadFile

from app.api.schemas.upload import UploadResponseSchema
from app.core.bootstrap import ingestion_service
from app.validators.upload_validator import validate_upload


router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponseSchema,
)
async def upload_document(
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

    finally:
        if (
            temp_path is not None
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)