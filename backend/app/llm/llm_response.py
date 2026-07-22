"""
LLM response model.

Defines the provider-agnostic response object returned by an LLM
implementation.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Represents the normalized response returned by an LLM.

    Attributes:
        content: The generated response text.
        input_tokens: Number of input (prompt) tokens consumed.
        output_tokens: Number of output (completion) tokens generated.
        total_tokens: Total number of tokens consumed.
        finish_reason: Reason the model stopped generating.
    """

    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    finish_reason: str | None = None