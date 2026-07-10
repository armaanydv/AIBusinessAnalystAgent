from typing import Optional

from app.models.document_element import DocumentElement


class Picture(DocumentElement):
    """
    Represents an image extracted from a document.
    """

    image_path: Optional[str] = None

    caption: Optional[str] = None

    alt_text: Optional[str] = None

    has_image: bool = False