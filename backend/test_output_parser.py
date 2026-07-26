"""
Tests for the generic OutputParser.
"""

import pytest

from app.exceptions.output_validation_exception import (
    OutputValidationException,
)
from app.llm.llm_response import LLMResponse
from app.llm.output_parser import OutputParser
from app.outputs.rag_answer import RAGAnswer


def test_parse_valid_rag_answer():
    """
    Parser should successfully convert valid JSON into a RAGAnswer.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "Tesla revenue increased by 14%.",
            "supporting_evidence": [
                "Revenue increased by 14%.",
                "Q4 report."
            ],
            "confidence": 0.91
        }
        """
    )

    result = OutputParser.parse(response, RAGAnswer)

    assert isinstance(result, RAGAnswer)
    assert result.answer == "Tesla revenue increased by 14%."
    assert result.confidence == 0.91
    assert len(result.supporting_evidence) == 2


def test_parse_invalid_json():
    """
    Parser should raise an exception when JSON is malformed.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "Hello"
        """
    )

    with pytest.raises(OutputValidationException):
        OutputParser.parse(response, RAGAnswer)


def test_parse_missing_required_field():
    """
    Parser should fail when a required field is missing.
    """

    response = LLMResponse(
        text="""
        {
            "supporting_evidence": [],
            "confidence": 0.85
        }
        """
    )

    with pytest.raises(OutputValidationException):
        OutputParser.parse(response, RAGAnswer)


def test_parse_invalid_field_type():
    """
    Parser should fail when a field has an invalid type.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "Example answer",
            "supporting_evidence": [],
            "confidence": "very high"
        }
        """
    )

    with pytest.raises(OutputValidationException):
        OutputParser.parse(response, RAGAnswer)


def test_parse_confidence_out_of_range():
    """
    Parser should fail when confidence is outside the allowed range.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "Example answer",
            "supporting_evidence": [],
            "confidence": 1.5
        }
        """
    )

    with pytest.raises(OutputValidationException):
        OutputParser.parse(response, RAGAnswer)


def test_parse_empty_supporting_evidence():
    """
    Empty evidence should still produce a valid RAGAnswer.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "No supporting evidence found.",
            "supporting_evidence": [],
            "confidence": 0.60
        }
        """
    )

    result = OutputParser.parse(response, RAGAnswer)

    assert isinstance(result, RAGAnswer)
    assert result.supporting_evidence == []
    assert result.confidence == 0.60


def test_parse_extra_fields_are_ignored():
    """
    Extra JSON fields should not break parsing.
    """

    response = LLMResponse(
        text="""
        {
            "answer": "Example answer",
            "supporting_evidence": [],
            "confidence": 0.95,
            "extra_field": "ignored"
        }
        """
    )

    result = OutputParser.parse(response, RAGAnswer)

    assert result.answer == "Example answer"
    assert result.confidence == 0.95
