"""
LLM request model.

Defines the provider-agnostic request object passed from the service
layer to an LLM implementation.
"""

from dataclasses import dataclass
from enum import Enum


class ResponseFormat(str, Enum):
    """
    Supported response formats from the LLM.
    """

    TEXT = "text"
    JSON = "json"


@dataclass(slots=True, frozen=True)
class LLMRequest:
    """
    Represents a single request to an LLM.

    Attributes:
        prompt: The fully constructed prompt.
        temperature: Optional override for the default sampling temperature.
        max_tokens: Optional override for the default maximum output tokens.
        response_format: Desired format of the model response.
    """

    prompt: str
    temperature: float | None = None
    max_tokens: int | None = None
    response_format: ResponseFormat = ResponseFormat.TEXT