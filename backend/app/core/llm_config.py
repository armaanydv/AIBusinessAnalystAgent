"""
LLM runtime configuration.

This module defines the immutable configuration object used by LLM
implementations. It is independent of environment variables and
application settings.
"""

from dataclasses import dataclass

from app.core.settings import get_settings


@dataclass(slots=True, frozen=True)
class LLMConfig:
    """
    Immutable runtime configuration for an LLM instance.
    """

    model: str
    temperature: float
    max_tokens: int
    timeout: float


def get_llm_config() -> LLMConfig:
    """
    Build an LLMConfig from application settings.
    """

    settings = get_settings()

    return LLMConfig(
        model=settings.llm.model,
        temperature=settings.llm.temperature,
        max_tokens=settings.llm.max_tokens,
        timeout=settings.llm.timeout,
    )