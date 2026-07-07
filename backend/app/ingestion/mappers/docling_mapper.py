from uuid import uuid4

from app.models.bounding_box import BoundingBox
from app.models.heading import Heading
from app.models.metadata import Metadata
from app.models.page import Page
from app.models.structured_document import StructuredDocument
from app.models.table import Table
from app.models.text_block import TextBlock


class DoclingMapper:
    """
    Maps a DoclingDocument into AIBA's StructuredDocument.
    """

    # ==========================================================
    # Public API
    # ==========================================================

    def map(self, docling_document) -> StructuredDocument:

        metadata = self._map_metadata(docling_document)
        pages = self._map_pages(docling_document)

        page_lookup = self._build_page_lookup(pages)

        self._map_texts(docling_document, page_lookup)
        self._map_tables(docling_document, page_lookup)

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

    def _build_page_lookup(self, pages) -> dict[int, Page]:

        return {
            page.page_number: page
            for page in pages
        }

    # ==========================================================
    # Shared Helpers
    # ==========================================================

    def _create_bounding_box(self, bbox):

        return BoundingBox(
            left=bbox.l,
            top=bbox.t,
            right=bbox.r,
            bottom=bbox.b,
        )

    # ==========================================================
    # Text Mapping
    # ==========================================================

    def _map_texts(self, docling_document, page_lookup):

        reading_order = 0

        for text_item in docling_document.texts:

            if not text_item.prov:
                continue

            prov = text_item.prov[0]

            bbox = self._create_bounding_box(prov.bbox)

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

    # ==========================================================
    # Table Mapping
    # ==========================================================

    def _map_tables(self, docling_document, page_lookup):

        reading_order = 0

        for table in docling_document.tables:

            if not table.prov:
              continue

            element = self._create_table(
            table,
            reading_order
        )

            page_lookup[element.page_number].elements.append(element)

            reading_order += 1

    def _create_table(self, table, reading_order):

       prov = table.prov[0]

       bbox = self._create_bounding_box(prov.bbox)

    # ---------------------------------------------------
    # Build exact visual grid
    # ---------------------------------------------------

       rows = [
        [""] * table.data.num_cols
        for _ in range(table.data.num_rows)
    ]

       for cell in table.data.table_cells:

          for r in range(
            cell.start_row_offset_idx,
            cell.start_row_offset_idx + cell.row_span
        ):

            for c in range(
                cell.start_col_offset_idx,
                cell.start_col_offset_idx + cell.col_span
            ):

                rows[r][c] = cell.text

    # ---------------------------------------------------
    # Headers
    # ---------------------------------------------------

       headers = rows[0] if rows else []

    # ---------------------------------------------------
    # Raw Text
    # ---------------------------------------------------

       raw_text = "\n".join(
        [
            " | ".join(row)
            for row in rows
        ]
    )

    # ---------------------------------------------------
    # Caption
    # ---------------------------------------------------

       caption = None

       if table.captions:
 
             caption = table.captions[0].text

    # ---------------------------------------------------
    # Return Table
    # ---------------------------------------------------

       return Table(
        page_number=prov.page_no,
        bounding_box=bbox,
        reading_order=reading_order,
        headers=headers,
        rows=rows,
        raw_text=raw_text,
        caption=caption,
        num_rows=table.data.num_rows,
        num_columns=table.data.num_cols,
    )