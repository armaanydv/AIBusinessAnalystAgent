from uuid import uuid4

from app.models.bounding_box import BoundingBox
from app.models.heading import Heading
from app.models.metadata import Metadata
from app.models.page import Page
from app.models.structured_document import StructuredDocument
from app.models.text_block import TextBlock


class DoclingMapper:
    """
    Maps a DoclingDocument into AIBA's StructuredDocument.
    """

    def map(self, docling_document) -> StructuredDocument:

        metadata = self._map_metadata(docling_document)
        pages = self._map_pages(docling_document)

        page_lookup = self._build_page_lookup(pages)

        self._map_texts(docling_document, page_lookup)

        return StructuredDocument(
            metadata=metadata,
            pages=pages,
        )

    def _map_metadata(self, docling_document) -> Metadata:

        return Metadata(
            document_id=str(uuid4()),
            title=getattr(docling_document, "name", None),
            total_pages=docling_document.num_pages(),
        )

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

    def _build_page_lookup(self, pages) -> dict[int, Page]:

        return {
            page.page_number: page
            for page in pages
        }

    def _map_texts(self, docling_document, page_lookup) -> None:

        reading_order = 0

        for text_item in docling_document.texts:

            if not text_item.prov:
                continue

            prov = text_item.prov[0]

            bbox = BoundingBox(
                left=prov.bbox.l,
                top=prov.bbox.t,
                right=prov.bbox.r,
                bottom=prov.bbox.b,
            )

            if text_item.label.value == "section_header":

                element = Heading(
                    text=text_item.text,
                    level=getattr(text_item, "level", 1),
                    page_number=prov.page_no,
                    bounding_box=bbox,
                    reading_order=reading_order,
                )

            else:

                element = TextBlock(
                    text=text_item.text,
                    page_number=prov.page_no,
                    bounding_box=bbox,
                    reading_order=reading_order,
                )

            page_lookup[prov.page_no].elements.append(element)

            reading_order += 1