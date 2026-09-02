from fastapi import APIRouter, HTTPException

from app.api.schemas.knowledge_base import (
    KnowledgeBaseDocumentSchema,
    KnowledgeBaseResponseSchema,
)

from app.core.bootstrap import (
    artifact_storage,
)


router = APIRouter()


@router.get(
    "/knowledge-base",
    response_model=KnowledgeBaseResponseSchema,
)
def get_knowledge_base():
    """
    Return all documents currently stored in the
    AIBA Knowledge Base.
    """

    document_ids = artifact_storage.list_documents()

    documents = []

    for document_id in document_ids:

        try:

            metadata = artifact_storage.load_metadata(
                document_id
            )

            document_name = (
                metadata.source_file
                or metadata.title
                or document_id
            )

            documents.append(
                KnowledgeBaseDocumentSchema(
                    document_id=metadata.document_id,
                    document_name=document_name,
                    title=metadata.title,
                    source_file=metadata.source_file,
                    file_type=metadata.file_type,
                    total_pages=metadata.total_pages,
                    created_at=metadata.created_at,
                )
            )

        except FileNotFoundError:

            continue

    return KnowledgeBaseResponseSchema(
        documents=documents,
        total_documents=len(documents),
    )


@router.delete(
    "/knowledge-base/{document_id}",
)
def delete_knowledge_base_document(
    document_id: str,
):
    """
    Delete a document from the AIBA Knowledge Base.
    """

    if not artifact_storage.document_exists(
        document_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    artifact_storage.delete_document(
        document_id
    )

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id,
    }