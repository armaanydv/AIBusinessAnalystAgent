from abc import ABC, abstractmethod

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BaseFusion(ABC):
    """
    Base interface for retrieval fusion strategies.
    """

    @abstractmethod
    def fuse(
        self,
        result_sets: list[list[RetrievalResult]],
        k: int,
    ) -> list[RetrievalResult]:
        """
        Fuse multiple ranked retrieval result sets into a single ranking.

        Args:
            result_sets:
                Multiple ranked retrieval result lists.

            k:
                Number of final results to return.

        Returns:
            A fused ranked list of RetrievalResults.
        """

        raise NotImplementedError