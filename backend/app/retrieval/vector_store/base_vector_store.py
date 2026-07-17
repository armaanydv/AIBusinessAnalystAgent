from abc import ABC, abstractmethod
from pathlib import Path

from app.retrieval.vector_store.vector_record import VectorRecord


class BaseVectorStore(ABC):
    """
    Abstract interface for vector database implementations.
    """

    @abstractmethod
    def add(
        self,
        record: VectorRecord,
    ) -> None:
        """
        Add a single vector to the store.
        """
        ...

    @abstractmethod
    def add_many(
        self,
        records: list[VectorRecord],
    ) -> None:
        """
        Add multiple vectors to the store.
        """
        ...

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[tuple[str, float]]:
        """
        Search for the top-k most similar vectors.

        Returns:
            List of (chunk_id, similarity_score)
        """
        ...

    @abstractmethod
    def save(
        self,
        directory: str | Path,
    ) -> None:
        """
        Persist the vector store to disk.
        """
        ...

    @abstractmethod
    def load(
        self,
        directory: str | Path,
    ) -> None:
        """
        Load a previously saved vector store.
        """
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        """
        Number of indexed vectors.
        """
        ...