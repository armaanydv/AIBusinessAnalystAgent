from pydantic import BaseModel, ConfigDict

from app.document.chunking.chunk import Chunk


class RerankResult(BaseModel):
    """
    Represents a reranked retrieval result.
    """

    chunk: Chunk

    retrieval_score: float

    rerank_score: float

    rank: int

    model_config = ConfigDict(
        frozen=True,
    )