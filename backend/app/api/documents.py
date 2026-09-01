from fastapi import APIRouter

from app.api.schemas.documents import (
    DocumentListResponseSchema,
    DocumentSummarySchema,
)
from app.core.bootstrap import artifact_storage


router = APIRouter()


@router.get(
    "/documents",
    response_model=DocumentListResponseSchema,
)
def list_documents():
    """
    Return all documents currently stored in the
    AIBA Knowledge Base.
    """

    document_ids = artifact_storage.list_documents()

    documents = []

    for document_id in document_ids:

        metadata = artifact_storage.load_metadata(
            document_id
        )

        documents.append(
            DocumentSummarySchema(
                document_id=metadata.document_id,
                title=metadata.title,
                source_file=metadata.source_file,
                file_type=metadata.file_type,
                total_pages=metadata.total_pages,
                created_at=metadata.created_at,
            )
        )

    return DocumentListResponseSchema(
        documents=documents,
        total_documents=len(documents),
    )