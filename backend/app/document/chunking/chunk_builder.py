from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection
from app.document.chunking.chunk_metadata import ChunkMetadata
from app.document.chunking.text_renderer import TextRenderer
from app.models.heading import Heading


class ChunkBuilder:
    """
    Builds semantic chunks from the hierarchy tree.
    """

    def __init__(self):

        self.renderer = TextRenderer()

    def build(self, structured_document) -> ChunkCollection:

        collection = ChunkCollection()

        hierarchy = structured_document.hierarchy_tree

        if hierarchy is None:
            return collection

        for section in hierarchy.root.children:

            elements = []

            title = None

            if section.element is not None:

                elements.append(section.element)

                if isinstance(section.element, Heading):
                    title = section.element.text

            for child in section.children:

                if child.element is not None:
                    elements.append(child.element)

            if not elements:
                continue

            text = self.renderer.render(elements)

            metadata = ChunkMetadata(
                start_page=min(e.page_number for e in elements),
                end_page=max(e.page_number for e in elements),
                hierarchy_level=1,
                character_count=len(text),
            )

            chunk = Chunk(
                title=title,
                text=text,
                metadata=metadata,
                source_element_ids=[e.id for e in elements],
            )

            collection.chunks.append(chunk)

        return collection