from uuid import uuid4

from app.ingestion.mappers.item_mapper_factory import ItemMapperFactory
from app.models.metadata import Metadata
from app.models.page import Page
from app.models.structured_document import StructuredDocument


class DoclingMapper:

    def __init__(self):

        self.factory = ItemMapperFactory()

    def map(self, docling_document):

        metadata = self._map_metadata(docling_document)

        pages = self._map_pages(docling_document)

        page_lookup = {
            page.page_number: page
            for page in pages
        }

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

            page_lookup[element.page_number].elements.append(element)

            reading_order += 1

        return StructuredDocument(
            metadata=metadata,
            pages=pages,
        )

    def _map_metadata(self, docling_document):

        return Metadata(
            document_id=str(uuid4()),
            title=getattr(docling_document, "name", None),
            total_pages=docling_document.num_pages(),
        )

    def _map_pages(self, docling_document):

        return [
            Page(page_number=i)
            for i in range(1, docling_document.num_pages() + 1)
        ]