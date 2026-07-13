from __future__ import annotations

from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.models.document_element import DocumentElement


class HierarchyNode(BaseModel):
    """
    Represents a node in the document hierarchy.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    # Virtual root has no document element
    element: Optional[DocumentElement] = None

    # Hierarchy depth (Root = 0)
    level: int = 0

    parent: Optional["HierarchyNode"] = None

    children: list["HierarchyNode"] = Field(default_factory=list)

    def add_child(self, child: "HierarchyNode") -> None:
        """
        Attach a child node.
        """

        child.parent = self
        self.children.append(child)


HierarchyNode.model_rebuild()