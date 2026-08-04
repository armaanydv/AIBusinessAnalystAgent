"""
Factory for creating LLM implementations.
"""

from google import genai
from groq import Groq

from app.core.llm_config import get_llm_config
from app.llm.base_llm import BaseLLM
from app.llm.gemini_llm import GeminiLLM
from app.llm.groq_llm import GroqLLM


class LLMFactory:
    """
    Factory responsible for creating the configured LLM.
    """

    @staticmethod
    def create() -> BaseLLM:

        config = get_llm_config()

        if config.provider == "gemini":

            client = genai.Client(
                api_key=config.api_key,
            )

            return GeminiLLM(
                client=client,
                config=config,
            )

        if config.provider == "groq":

            client = Groq(
                api_key=config.api_key,
            )

            return GroqLLM(
                client=client,
                config=config,
            )

        raise ValueError(
            f"Unsupported LLM provider: {config.provider}"
        )