from app.ingestion.parsers.docling_parser import DoclingParser
from app.preprocessing.document_preprocessor import document_preprocessor


class IngestionService:

    def __init__(self):
        self.parser = DoclingParser()

    def ingest(self, file_path):

        raw_document = self.parser.parse(file_path)

        clean_document = document_preprocessor.preprocess(raw_document)

        return clean_document


ingestion_service = IngestionService()