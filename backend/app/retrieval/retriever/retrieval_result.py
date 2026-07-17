from dataclasses import dataclass

from app.document.chunking.chunk import Chunk


@dataclass(slots=True, frozen=True)
class RetrievalResult:
    """
    Represents a single retrieval result returned by a retriever.
    """

    chunk: Chunk

    similarity_score: float