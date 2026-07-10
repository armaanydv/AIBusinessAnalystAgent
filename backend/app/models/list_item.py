from typing import Optional

from app.models.document_element import DocumentElement


class ListItem(DocumentElement):
    """
    Represents a list item extracted from a document.
    """

    text: str

    marker: str

    enumerated: bool = False

    hyperlink: Optional[str] = None