from app.models.structured_document import StructuredDocument


class DoclingMapper:

    def map(self, docling_output) -> StructuredDocument:

        return StructuredDocument(
            text="Dummy parsed document"
        )