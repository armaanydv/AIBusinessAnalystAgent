from typing import Optional

from pydantic import BaseModel, Field

from app.document.hierarchy.hierarchy_tree import HierarchyTree
from app.document.indexing.document_index import DocumentIndex
from app.document.relationships.relationship_graph import RelationshipGraph
from app.models.metadata import Metadata
from app.models.page import Page


class StructuredDocument(BaseModel):
    """
    Root model representing an entire parsed document.
    """

    metadata: Metadata

    pages: list[Page] = Field(default_factory=list)

    # Fast lookup indexes
    index: Optional[DocumentIndex] = None

    # Relationships between document elements
    relationship_graph: Optional[RelationshipGraph] = None

    # Logical hierarchy of the document
    hierarchy_tree: Optional[HierarchyTree] = None