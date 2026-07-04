from app.ingestion.parsers.base_parser import BaseParser
from app.ingestion.parsers.mappers.docling_mapper import DoclingMapper


class DoclingParser(BaseParser):

    def __init__(self):
        self.mapper = DoclingMapper()

    def parse(self, file_path: str):

        # Placeholder for Docling output
        docling_output = {}

        return self.mapper.map(docling_output)