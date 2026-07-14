from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.document.chunking.chunk_metadata import ChunkMetadata


class Chunk(BaseModel):
    """
    Represents one semantic chunk of a document.
    """

    # ==========================================================
    # Identity
    # ==========================================================

    id: str = Field(default_factory=lambda: str(uuid4()))

    # ==========================================================
    # Content
    # ==========================================================

    title: Optional[str] = None

    text: str

    # ==========================================================
    # Traceability
    # ==========================================================

    source_element_ids: list[str] = Field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: ChunkMetadata