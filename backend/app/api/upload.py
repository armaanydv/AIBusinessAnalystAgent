from pathlib import Path
import os
import tempfile

from fastapi import APIRouter, File, UploadFile

from app.api.schemas.upload import UploadResponseSchema
from app.core.bootstrap import (
    artifact_storage,
    ingestion_service,
)
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
        # Enrich metadata with original upload information
        # ---------------------------------------------------------

        original_path = Path(file.filename)

        document.metadata.title = original_path.stem
        document.metadata.source_file = original_path.name
        document.metadata.file_type = (
            original_path.suffix.lstrip(".").lower()
        )

        # ---------------------------------------------------------
        # Persist updated metadata
        # ---------------------------------------------------------

        artifact_storage.save_metadata(
            document_id=document.metadata.document_id,
            metadata=document.metadata,
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