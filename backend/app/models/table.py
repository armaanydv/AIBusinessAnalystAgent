from typing import List, Optional

from app.models.document_element import DocumentElement


class Table(DocumentElement):
    """
    Represents a table extracted from a document.
    """

    headers: List[str] = []

    rows: List[List[str]] = []

    raw_text: str = ""

    caption: Optional[str] = None

    num_rows: int = 0

    num_columns: int = 0