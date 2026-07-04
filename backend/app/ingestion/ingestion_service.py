from app.ingestion.parsers.docling_parser import DoclingParser


class IngestionService:

    def __init__(self):
        self.parser = DoclingParser()

    def ingest(self, file_path: str):

        return self.parser.parse(file_path)


ingestion_service = IngestionService()