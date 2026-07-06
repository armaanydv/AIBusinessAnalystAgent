from typing import List

from app.models.document_element import DocumentElement


class Table(DocumentElement):
    """
    Represents a table extracted from a document.
    """

    rows: List[List[str]]

    raw_text: str

    num_rows: int

    num_columns: int