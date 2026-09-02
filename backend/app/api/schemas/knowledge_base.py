from pydantic import BaseModel


class KnowledgeBaseDocumentSchema(BaseModel):
    """
    Represents a document displayed in the AIBA Knowledge Base.
    """

    document_id: str

    document_name: str

    title: str | None = None
    source_file: str | None = None
    file_type: str | None = None

    total_pages: int = 0

    created_at: str | None = None


class KnowledgeBaseResponseSchema(BaseModel):
    """
    Response containing all documents in the AIBA Knowledge Base.
    """

    documents: list[KnowledgeBaseDocumentSchema]

    total_documents: int