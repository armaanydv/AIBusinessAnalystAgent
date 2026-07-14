from pydantic import BaseModel, Field

from app.document.chunking.chunk import Chunk


class ChunkCollection(BaseModel):
    """
    Collection of semantic chunks belonging to a document.
    """

    chunks: list[Chunk] = Field(default_factory=list)