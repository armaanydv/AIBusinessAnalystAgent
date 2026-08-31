from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    """
    Standard error response returned by the API.
    """

    detail: str