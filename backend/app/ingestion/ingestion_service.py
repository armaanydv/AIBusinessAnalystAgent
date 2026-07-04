from app.ingestion.parsers.docling_parser import DoclingParser


class IngestionService:

    def __init__(self):
        self.parser = DoclingParser()

    def ingest(self):

        structured_document = self.parser.parse("dummy.pdf")

        return {
            "message": "Document ingested successfully.",
            "document": structured_document.text
        }


ingestion_service = IngestionService()