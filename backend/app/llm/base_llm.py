"""
Base interface for all LLM implementations.
"""

from abc import ABC, abstractmethod

from app.llm.llm_request import LLMRequest
from app.llm.llm_response import LLMResponse


class BaseLLM(ABC):
    """
    Abstract base class for all Large Language Model providers.
    """

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a response for the given request.

        Args:
            request: The LLM request.

        Returns:
            A normalized LLMResponse.
        """
        raise NotImplementedError