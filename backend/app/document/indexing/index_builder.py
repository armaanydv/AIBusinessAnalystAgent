from app.document.indexing.document_index import DocumentIndex
from app.models.structured_document import StructuredDocument


class IndexBuilder:
    """
    Builds lookup indexes for a StructuredDocument.
    """

    def build(self, document: StructuredDocument) -> DocumentIndex:

        index = DocumentIndex()

        for page in document.pages:

            index.by_page[page.page_number] = page.elements

            for element in page.elements:

                index.by_element_id[element.id] = element

                if element.docling_ref is not None:
                    index.by_docling_ref[element.docling_ref] = element

        return index