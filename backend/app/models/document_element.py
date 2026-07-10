from abc import ABC
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.models.bounding_box import BoundingBox


class DocumentElement(BaseModel, ABC):
    """
    Base class for every element present in a document.
    """

    # ==========================================================
    # AIBA Identity
    # ==========================================================

    id: str = Field(default_factory=lambda: str(uuid4()))

    # ==========================================================
    # Docling Identity
    # ==========================================================

    docling_ref: Optional[str] = None

    # ==========================================================
    # Location
    # ==========================================================

    page_number: int

    bounding_box: Optional[BoundingBox] = None

    # ==========================================================
    # Reading Order
    # ==========================================================

    reading_order: int

    # ==========================================================
    # Confidence
    # ==========================================================

    confidence: Optional[float] = None