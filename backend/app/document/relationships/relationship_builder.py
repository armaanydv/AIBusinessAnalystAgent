from app.document.relationships.relationship import Relationship
from app.document.relationships.relationship_graph import RelationshipGraph
from app.document.relationships.relationship_type import RelationshipType


class RelationshipBuilder:
    """
    Builds relationships between document elements using the
    original Docling document and the AIBA document index.
    """

    def build(self, docling_document, structured_document):

        graph = RelationshipGraph()

        index = structured_document.index

        if index is None:
            return graph

        for node, level in docling_document.iterate_items():

            source = index.by_docling_ref.get(node.self_ref)

            if source is None:
                continue

            self._process_children(
                node,
                source.id,
                graph,
                index,
            )

            self._process_captions(
                node,
                source.id,
                graph,
                index,
            )

            self._process_references(
                node,
                source.id,
                graph,
                index,
            )

            self._process_footnotes(
                node,
                source.id,
                graph,
                index,
            )

        return graph

    # ==========================================================
    # Children
    # ==========================================================

    def _process_children(
        self,
        node,
        source_id,
        graph,
        index,
    ):

        if not hasattr(node, "children"):
            return

        for ref in node.children:

            target = index.by_docling_ref.get(ref.cref)

            if target is None:
                continue

            graph.add_relationship(
                Relationship(
                    source_id=source_id,
                    target_id=target.id,
                    relationship_type=RelationshipType.CONTAINS,
                )
            )

    # ==========================================================
    # Captions
    # ==========================================================

    def _process_captions(
        self,
        node,
        source_id,
        graph,
        index,
    ):

        if not hasattr(node, "captions"):
            return

        for ref in node.captions:

            target = index.by_docling_ref.get(ref.cref)

            if target is None:
                continue

            graph.add_relationship(
                Relationship(
                    source_id=source_id,
                    target_id=target.id,
                    relationship_type=RelationshipType.CAPTION,
                )
            )

    # ==========================================================
    # References
    # ==========================================================

    def _process_references(
        self,
        node,
        source_id,
        graph,
        index,
    ):

        if not hasattr(node, "references"):
            return

        for ref in node.references:

            target = index.by_docling_ref.get(ref.cref)

            if target is None:
                continue

            graph.add_relationship(
                Relationship(
                    source_id=source_id,
                    target_id=target.id,
                    relationship_type=RelationshipType.REFERENCE,
                )
            )

    # ==========================================================
    # Footnotes
    # ==========================================================

    def _process_footnotes(
        self,
        node,
        source_id,
        graph,
        index,
    ):

        if not hasattr(node, "footnotes"):
            return

        for ref in node.footnotes:

            target = index.by_docling_ref.get(ref.cref)

            if target is None:
                continue

            graph.add_relationship(
                Relationship(
                    source_id=source_id,
                    target_id=target.id,
                    relationship_type=RelationshipType.FOOTNOTE,
                )
            )