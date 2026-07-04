from docling.document_converter import DocumentConverter

from app.ingestion.parsers.base_parser import BaseParser
from app.ingestion.mappers.docling_mapper import DoclingMapper
from app.models.structured_document import StructuredDocument


class DoclingParser(BaseParser):

    def __init__(self):
        self.converter = DocumentConverter()
        self.mapper = DoclingMapper()

    def parse(self, file_path: str):

        print("Creating converter...")

        result = self.converter.convert(file_path)

        print("Conversion complete!")

        return self.mapper.map(result.document)