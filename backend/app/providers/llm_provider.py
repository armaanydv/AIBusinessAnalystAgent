"""
LLM provider.

Responsible for constructing and providing configured LLM instances.
"""

from google import genai

from app.core.llm_config import LLMConfig
from app.core.settings import get_settings
from app.llm.base_llm import BaseLLM
from app.llm.gemini_llm import GeminiLLM


def get_llm() -> BaseLLM:
    """
    Create and return a configured LLM instance.

    Returns:
        A configured BaseLLM implementation.
    """

    settings = get_settings()

    config = LLMConfig(
        model=settings.llm.model,
        temperature=settings.llm.temperature,
        max_tokens=settings.llm.max_tokens,
        timeout=settings.llm.timeout,
    )

    client = genai.Client(
        api_key=settings.llm.api_key,
    )

    return GeminiLLM(
        client=client,
        config=config,
    )