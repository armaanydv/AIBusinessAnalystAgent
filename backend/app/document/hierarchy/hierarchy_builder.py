from app.document.hierarchy.hierarchy_node import HierarchyNode
from app.document.hierarchy.hierarchy_tree import HierarchyTree
from app.models.heading import Heading


class HierarchyBuilder:
    """
    Builds the logical hierarchy of a StructuredDocument.

    Version 1:
    Every heading starts a new top-level section.
    Every subsequent non-heading element belongs to that heading
    until another heading is encountered.
    """

    def build(self, structured_document) -> HierarchyTree:

        tree = HierarchyTree()

        root = tree.root

        current_parent = root

        for page in structured_document.pages:

            for element in page.elements:

                node = HierarchyNode(
                    element=element,
                )

                # --------------------------------------------------
                # Heading starts a new section
                # --------------------------------------------------

                if isinstance(element, Heading):

                    root.add_child(node)

                    current_parent = node

                # --------------------------------------------------
                # Normal document element
                # --------------------------------------------------

                else:

                    current_parent.add_child(node)

        return tree