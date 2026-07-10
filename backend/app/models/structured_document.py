from typing import Optional

from pydantic import BaseModel, Field

from app.document.indexing.document_index import DocumentIndex
from app.models.metadata import Metadata
from app.models.page import Page


class StructuredDocument(BaseModel):
    """
    Root model representing an entire parsed document.
    """

    metadata: Metadata

    pages: list[Page] = Field(default_factory=list)

    index: Optional[DocumentIndex] = None