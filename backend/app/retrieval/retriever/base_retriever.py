from abc import ABC, abstractmethod

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BaseRetriever(ABC):
    """
    Abstract interface for all document retrievers.

    A retriever accepts a user query and returns the most
    relevant document chunks.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k most relevant chunks.

        Args:
            query:
                User's natural language query.

            k:
                Number of chunks to retrieve.

        Returns:
            List of retrieval results sorted by descending
            similarity score.
        """
        ...