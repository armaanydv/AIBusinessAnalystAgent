from pydantic import BaseModel


class DocumentSummarySchema(BaseModel):
    """
    Summary information about a document in the
    AIBA Knowledge Base.
    """

    document_id: str

    title: str | None

    source_file: str | None

    file_type: str | None

    total_pages: int

    created_at: str | None


class DocumentListResponseSchema(BaseModel):
    """
    Response returned when listing all documents
    in the Knowledge Base.
    """

    documents: list[DocumentSummarySchema]

    total_documents: int