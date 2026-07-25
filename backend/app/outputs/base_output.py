from datetime import datetime

from pydantic import BaseModel, Field


class BaseOutput(BaseModel):
    """
    Base class for all structured LLM outputs.

    Every response produced by AIBA should inherit from this model.
    """

    model_version: str = Field(
        default="1.0",
        description="Schema version of the output.",
    )

    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the output was generated.",
    )