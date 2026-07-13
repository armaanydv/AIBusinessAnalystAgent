from pydantic import BaseModel, Field

from app.document.hierarchy.hierarchy_node import HierarchyNode


class HierarchyTree(BaseModel):
    """
    Represents the logical hierarchy of a document.
    """

    root: HierarchyNode = Field(
        default_factory=lambda: HierarchyNode(level=0)
    )