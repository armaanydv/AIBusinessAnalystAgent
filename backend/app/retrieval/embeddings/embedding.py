from uuid import uuid4

from pydantic import BaseModel, Field


class Embedding(BaseModel):
    """
    Represents the vector embedding of a semantic chunk.
    """

    # ==========================================================
    # Identity
    # ==========================================================

    id: str = Field(default_factory=lambda: str(uuid4()))

    # ==========================================================
    # Source
    # ==========================================================

    chunk_id: str

    # ==========================================================
    # Embedding
    # ==========================================================

    vector: list[float]

    # ==========================================================
    # Metadata
    # ==========================================================

    model_name: str

    dimension: int