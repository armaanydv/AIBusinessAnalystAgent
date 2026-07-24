import logging

from docling.document_converter import DocumentConverter

from app.ingestion.parsed_document import ParsedDocument
from app.ingestion.parsers.base_parser import BaseParser
from app.ingestion.mappers.docling_mapper import DoclingMapper

logger = logging.getLogger(__name__)


class DoclingParser(BaseParser):

    def __init__(self):
        self.converter = DocumentConverter()
        self.mapper = DoclingMapper()

    def parse(self, file_path: str) -> ParsedDocument:

        logger.info("Parsing document: %s", file_path)

        result = self.converter.convert(file_path)

        logger.info("Document conversion completed.")

        structured_document = self.mapper.map(result.document)

        return ParsedDocument(
            docling_document=result.document,
            structured_document=structured_document,
        )