from abc import ABC, abstractmethod

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BasePromptBuilder(ABC):
    """
    Abstract interface for prompt builders.

    A prompt builder converts a user query and retrieved
    document chunks into a prompt ready for an LLM.
    """

    @abstractmethod
    def build(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
    ) -> str:
        """
        Build the prompt.

        Args:
            query:
                User question.

            retrieval_results:
                Retrieved chunks.

        Returns:
            Prompt string.
        """
        ...