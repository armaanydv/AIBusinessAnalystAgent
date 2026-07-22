"""
Custom exceptions for the LLM layer.
"""


class LLMError(Exception):
    """
    Base exception for all LLM-related errors.
    """


class LLMGenerationError(LLMError):
    """
    Raised when the LLM fails to generate a response.
    """


class LLMConfigurationError(LLMError):
    """
    Raised when the LLM is configured incorrectly.
    """


class LLMAuthenticationError(LLMError):
    """
    Raised when authentication with the LLM provider fails.
    """


class LLMRateLimitError(LLMError):
    """
    Raised when the provider's rate limit is exceeded.
    """


class LLMTimeoutError(LLMError):
    """
    Raised when an LLM request times out.
    """