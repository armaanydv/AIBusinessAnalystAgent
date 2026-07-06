from typing import Optional

from app.models.document_element import DocumentElement


class TextBlock(DocumentElement):
    """
    Represents a block of textual content in the document.
    """

    text: str

    font_size: Optional[float] = None
    font_name: Optional[str] = None

    is_bold: bool = False
    is_italic: bool = False