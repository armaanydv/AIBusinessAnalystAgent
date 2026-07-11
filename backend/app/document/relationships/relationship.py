from uuid import uuid4

from pydantic import BaseModel, Field

from app.document.relationships.relationship_type import RelationshipType


class Relationship(BaseModel):
    """
    Represents a relationship between two document elements.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    source_id: str

    target_id: str

    relationship_type: RelationshipType