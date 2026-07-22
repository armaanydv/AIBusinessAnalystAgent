"""
LLM runtime configuration.

This module defines the immutable configuration object used by LLM
implementations. It is independent of environment variables and
application settings.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMConfig:
    """
    Immutable runtime configuration for an LLM instance.

    Attributes:
        model: Default model name.
        temperature: Default sampling temperature.
        max_tokens: Default maximum number of output tokens.
        timeout: Request timeout in seconds.
    """

    model: str
    temperature: float
    max_tokens: int
    timeout: float