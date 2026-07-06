from typing import Optional

from app.models.document_element import DocumentElement


class Formula(DocumentElement):
    """
    Represents a mathematical formula extracted from a document.
    """

    latex: Optional[str] = None

    plain_text: str