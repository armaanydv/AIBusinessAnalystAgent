"""
Custom exception raised when an LLM response cannot be parsed into
the expected structured output.
"""


class OutputValidationException(Exception):
    """
    Raised when structured output validation fails.
    """

    pass