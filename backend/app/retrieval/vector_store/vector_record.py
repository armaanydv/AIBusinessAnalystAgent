from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class VectorRecord:
    """
    Represents a vector stored inside the vector database.

    This is an infrastructure model used by the vector store.
    It intentionally contains only the data required for indexing
    and retrieval, independent of the embedding model.
    """

    chunk_id: str

    vector: list[float]

    metadata: dict[str, Any] = field(default_factory=dict)