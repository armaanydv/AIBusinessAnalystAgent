from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.structured_document import StructuredDocument


class ParsedDocument(BaseModel):
    """
    Represents the complete output of the parsing stage.
    """

    docling_document: Any
    structured_document: StructuredDocument

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )