from typing import Optional

from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    """
    Metadata describing a semantic chunk.
    """

    # Page range covered by this chunk
    start_page: int

    end_page: int

    # Hierarchy depth
    hierarchy_level: int = 1

    # Reserved for embedding stage
    token_count: Optional[int] = None

    character_count: Optional[int] = None