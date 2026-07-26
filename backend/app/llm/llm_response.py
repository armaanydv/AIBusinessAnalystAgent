"""
LLM response model.

Defines the provider-agnostic response object returned by any
Large Language Model implementation.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Represents a normalized response returned by an LLM provider.

    This model acts as a provider-independent contract between the
    LLM layer and the rest of the application.

    Attributes:
        text:
            Generated response text.

        input_tokens:
            Number of prompt tokens consumed.

        output_tokens:
            Number of completion tokens generated.

        total_tokens:
            Total number of tokens consumed.

        finish_reason:
            Reason why generation stopped
            (e.g. "STOP", "MAX_TOKENS").

        model_name:
            Name of the model that generated the response.

        latency_ms:
            Time taken by the provider to generate the response.

        metadata:
            Provider-specific metadata not required by the rest
            of the application.
    """

    text: str

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    finish_reason: str | None = None

    model_name: str | None = None

    latency_ms: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)