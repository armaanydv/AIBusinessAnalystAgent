from abc import ABC, abstractmethod

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BasePromptBuilder(ABC):
    """
    Abstract interface for all prompt builders.

    A prompt builder is responsible for converting a user query
    and retrieved document chunks into a prompt that can be
    consumed by an LLM.
    """

    @abstractmethod
    def build(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
    ) -> str:
        """
        Build the final prompt.

        Args:
            query:
                User question.

            retrieval_results:
                Retrieved document chunks.

        Returns:
            Complete prompt string.
        """
        pass