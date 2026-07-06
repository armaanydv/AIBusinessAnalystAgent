from typing import List

from pydantic import BaseModel, Field

from app.models.metadata import Metadata
from app.models.page import Page


class StructuredDocument(BaseModel):
    """
    Root model representing an entire parsed document.
    """

    metadata: Metadata

    pages: List[Page] = Field(default_factory=list)