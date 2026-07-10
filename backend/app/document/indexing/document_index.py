from pydantic import BaseModel, Field

from app.models.document_element import DocumentElement
from app.models.page import Page


class DocumentIndex(BaseModel):
    """
    Fast lookup indexes for a StructuredDocument.
    """

    by_element_id: dict[str, DocumentElement] = Field(default_factory=dict)

    by_docling_ref: dict[str, DocumentElement] = Field(default_factory=dict)

    by_page: dict[int, list[DocumentElement]] = Field(default_factory=dict)