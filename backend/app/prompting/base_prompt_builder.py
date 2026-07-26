"""
Base interface for prompt builders.
"""

from abc import ABC
from abc import abstractmethod

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BasePromptBuilder(ABC):
    """
    Abstract interface for all prompt builders.
    """

    @abstractmethod
    def build(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
    ) -> str:
        """
        Build a complete prompt for the LLM.

        Args:
            query:
                User query.

            retrieval_results:
                Retrieved document chunks.

        Returns:
            Fully formatted prompt.
        """
        raise NotImplementedError