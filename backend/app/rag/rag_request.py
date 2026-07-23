from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RAGRequest:
    """
    Represents a user request to the RAG pipeline.
    """

    query: str
    top_k: int = 5