from uuid import uuid4

from app.ingestion.mappers.item_mappers.item_mapper_factory import ItemMapperFactory
from app.models.metadata import Metadata
from app.models.page import Page
from app.models.structured_document import StructuredDocument


class DoclingMapper:
    """
    Maps a DoclingDocument into AIBA's StructuredDocument.
    """

    def __init__(self):

        self.factory = ItemMapperFactory()

    # ==========================================================
    # Public API
    # ==========================================================

    def map(self, docling_document) -> StructuredDocument:

        metadata = self._map_metadata(docling_document)

        pages = self._map_pages(docling_document)

        page_lookup = self._build_page_lookup(pages)

        reading_order = 0

        for node, level in docling_document.iterate_items():

            mapper = self.factory.get_mapper(node)

            if mapper is None:
                continue

            element = mapper.map(
                node=node,
                level=level,
                reading_order=reading_order,
            )

            if element is None:
                continue

            page_lookup[element.page_number].elements.append(
                element
            )

            reading_order += 1

        return StructuredDocument(
            metadata=metadata,
            pages=pages,
        )

    # ==========================================================
    # Metadata Mapping
    # ==========================================================

    def _map_metadata(self, docling_document) -> Metadata:

        return Metadata(
            document_id=str(uuid4()),
            title=getattr(docling_document, "name", None),
            total_pages=docling_document.num_pages(),
        )

    # ==========================================================
    # Page Mapping
    # ==========================================================

    def _map_pages(self, docling_document) -> list[Page]:

        pages = []

        total_pages = docling_document.num_pages()

        for page_number in range(1, total_pages + 1):

            pages.append(
                Page(
                    page_number=page_number,
                )
            )

        return pages

    # ==========================================================
    # Helpers
    # ==========================================================

    def _build_page_lookup(
        self,
        pages: list[Page],
    ) -> dict[int, Page]:

        return {
            page.page_number: page
            for page in pages
        }