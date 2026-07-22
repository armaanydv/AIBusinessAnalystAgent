"""
Gemini LLM implementation.
"""

from google import genai
from google.genai import types

from app.exceptions.llm_exceptions import LLMGenerationError
from app.llm.base_llm import BaseLLM
from app.core.llm_config import LLMConfig
from app.llm.llm_request import LLMRequest
from app.llm.llm_response import LLMResponse


class GeminiLLM(BaseLLM):
    """
    Google Gemini implementation of the BaseLLM interface.
    """

    def __init__(
        self,
        client: genai.Client,
        config: LLMConfig,
    ) -> None:
        self._client = client
        self._config = config

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a response using the Gemini API.

        Args:
            request: The request to send to Gemini.

        Returns:
            A normalized LLMResponse.

        Raises:
            LLMGenerationError:
                If Gemini fails to generate a response.
        """

        try:
            response = self._client.models.generate_content(
                model=self._config.model,
                contents=request.prompt,
                config=self._build_generation_config(request),
            )

            usage = getattr(response, "usage_metadata", None)

            return LLMResponse(
                content=response.text,
                input_tokens=getattr(usage, "prompt_token_count", None),
                output_tokens=getattr(usage, "candidates_token_count", None),
                total_tokens=getattr(usage, "total_token_count", None),
                finish_reason=(
                    response.candidates[0].finish_reason.name
                    if response.candidates
                    else None
                ),
            )

        except Exception as exc:
            raise LLMGenerationError(
                "Failed to generate response from Gemini."
            ) from exc

    def _build_generation_config(
        self,
        request: LLMRequest,
    ) -> types.GenerateContentConfig:
        """
        Build the Gemini generation configuration.
        """

        return types.GenerateContentConfig(
            temperature=(
                request.temperature
                if request.temperature is not None
                else self._config.temperature
            ),
            max_output_tokens=(
                request.max_tokens
                if request.max_tokens is not None
                else self._config.max_tokens
            ),
        )