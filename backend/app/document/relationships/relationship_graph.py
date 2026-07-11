from pydantic import BaseModel, Field

from app.document.relationships.relationship import Relationship


class RelationshipGraph(BaseModel):
    """
    Stores relationships between document elements.
    """

    relationships: list[Relationship] = Field(default_factory=list)

    def add_relationship(self, relationship: Relationship) -> None:
        self.relationships.append(relationship)