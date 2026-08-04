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

    provider: str

    model: str

    api_key: str

    temperature: float

    max_tokens: int

    timeout: float


def get_llm_config() -> LLMConfig:
    """
    Build an LLMConfig from application settings.
    """

    settings = get_settings()

    provider = settings.llm.provider.lower()

    if provider == "groq":

        return LLMConfig(
            provider="groq",
            model=settings.llm.groq_model,
            api_key=settings.llm.groq_api_key,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens,
            timeout=settings.llm.timeout,
        )

    if provider == "gemini":

        return LLMConfig(
            provider="gemini",
            model=settings.llm.gemini_model,
            api_key=settings.llm.gemini_api_key,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens,
            timeout=settings.llm.timeout,
        )

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )