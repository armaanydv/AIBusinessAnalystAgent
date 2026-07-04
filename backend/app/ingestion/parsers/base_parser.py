from abc import ABC, abstractmethod
from app.models.structured_document import StructuredDocument


class BaseParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> StructuredDocument:
        pass