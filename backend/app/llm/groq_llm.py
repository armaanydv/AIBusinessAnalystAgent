"""
Groq LLM implementation.
"""

from groq import Groq

from app.core.llm_config import LLMConfig
from app.exceptions.llm_exceptions import LLMGenerationError
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest
from app.llm.llm_response import LLMResponse


class GroqLLM(BaseLLM):
    """
    Groq implementation of the BaseLLM interface.
    """

    def __init__(
        self,
        client: Groq,
        config: LLMConfig,
    ) -> None:

        self._client = client
        self._config = config

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response using the Groq API.
        """

        try:

            response = (
                self._client.chat.completions.create(
                    model=self._config.model,
                    messages=[
                        {
                            "role": "user",
                            "content": request.prompt,
                        }
                    ],
                    temperature=(
                        request.temperature
                        if request.temperature is not None
                        else self._config.temperature
                    ),
                    max_tokens=(
                        request.max_tokens
                        if request.max_tokens is not None
                        else self._config.max_tokens
                    ),
                )
            )

            usage = response.usage

            choice = response.choices[0]

            return LLMResponse(
                text=choice.message.content,
                input_tokens=(
                    usage.prompt_tokens
                    if usage is not None
                    else None
                ),
                output_tokens=(
                    usage.completion_tokens
                    if usage is not None
                    else None
                ),
                total_tokens=(
                    usage.total_tokens
                    if usage is not None
                    else None
                ),
                finish_reason=choice.finish_reason,
            )

        except Exception as exc:
            raise LLMGenerationError(
                "Failed to generate response from Groq."
            ) from exc