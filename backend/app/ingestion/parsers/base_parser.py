from abc import ABC, abstractmethod

from app.ingestion.parsed_document import ParsedDocument


class BaseParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        pass