from abc import ABC, abstractmethod

from app.retrieval.retriever.retrieval_result import (
    RetrievalResult,
)
from app.retrieval.reranker.rerank_result import (
    RerankResult,
)


class BaseReranker(ABC):
    """
    Base interface for all rerankers.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
        k: int,
    ) -> list[RerankResult]:
        """
        Rerank retrieved chunks.

        Args:
            query:
                User query.

            retrieval_results:
                Results returned by the retriever.

            k:
                Number of results to return.

        Returns:
            Top-k reranked results.
        """

        raise NotImplementedError