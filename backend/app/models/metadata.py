from typing import Optional
from pydantic import BaseModel


class Metadata(BaseModel):
    """
    Stores document-level metadata.
    """

    document_id: str

    title: Optional[str] = None
    author: Optional[str] = None
    language: Optional[str] = None

    source_file: Optional[str] = None
    file_type: Optional[str] = None

    total_pages: int = 0

    created_at: Optional[str] = None
    modified_at: Optional[str] = None