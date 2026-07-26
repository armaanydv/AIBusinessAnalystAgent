"""
Generic parser for converting raw LLM responses into validated
structured output models.
"""

from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ValidationError

from app.exceptions.output_validation_exception import (
    OutputValidationException,
)
from app.llm.llm_response import LLMResponse

T = TypeVar("T", bound=BaseModel)


class OutputParser:
    """
    Parses an LLM response into a validated Pydantic model.

    This parser is completely generic and can be reused for any
    structured output model.
    """

    @staticmethod
    def parse(
        response: LLMResponse,
        output_model: type[T],
    ) -> T:
        """
        Parse an LLM response into the requested output model.

        Args:
            response:
                The normalized response returned by the LLM.

            output_model:
                The expected Pydantic model.

        Returns:
            A validated instance of the requested model.

        Raises:
            OutputValidationException:
                If the response is not valid JSON or does not
                conform to the expected schema.
        """

        try:
            data = json.loads(response.text)

            return output_model.model_validate(data)

        except json.JSONDecodeError as exc:
            raise OutputValidationException(
                "The LLM returned invalid JSON."
            ) from exc

        except ValidationError as exc:
            raise OutputValidationException(
                f"Failed to validate response as "
                f"{output_model.__name__}: {exc}"
            ) from exc