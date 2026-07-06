from typing import List

from pydantic import BaseModel, Field

from app.models.document_element import DocumentElement


class Page(BaseModel):
    """
    Represents a single page of a document.
    """

    page_number: int

    width: float = 0.0
    height: float = 0.0

    elements: List[DocumentElement] = Field(default_factory=list)