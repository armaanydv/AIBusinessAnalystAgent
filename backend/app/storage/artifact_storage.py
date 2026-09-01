from pathlib import Path

from app.core.settings import get_settings
from app.document.chunking.chunk_collection import ChunkCollection
from app.models.structured_document import StructuredDocument
from app.retrieval.bm25.bm25_index import BM25Index
from app.retrieval.vector_store.faiss_vector_store import (
    FAISSVectorStore,
)


class ArtifactStorage:
    """
    Persists and loads document artifacts.

    Directory layout:

    storage/
        <document_id>/
            structured_document.json
            chunks.json
            vector.index
            mapping.pkl
            bm25_index.json
    """

    DOCUMENT_FILENAME = "structured_document.json"
    CHUNKS_FILENAME = "chunks.json"

    def __init__(self) -> None:

        settings = get_settings()

        self._root_directory = Path(
            settings.storage.root_directory
        )

    # ---------------------------------------------------------
    # Paths
    # ---------------------------------------------------------

    def _document_directory(
        self,
        document_id: str,
    ) -> Path:

        return self._root_directory / document_id

    # ---------------------------------------------------------
    # Document Discovery
    # ---------------------------------------------------------

    def list_documents(
        self,
    ) -> list[str]:
        """
        Returns the IDs of all persisted documents.
        """

        if not self._root_directory.exists():
            return []

        return sorted(
            [
                directory.name
                for directory in self._root_directory.iterdir()
                if directory.is_dir()
            ]
        )

    def document_exists(
        self,
        document_id: str,
    ) -> bool:
        """
        Returns True if the document exists on disk.
        """

        return self._document_directory(
            document_id
        ).exists()

    # ---------------------------------------------------------
    # Structured Document
    # ---------------------------------------------------------

    def save_document(
        self,
        document_id: str,
        document: StructuredDocument,
    ) -> None:

        directory = self._document_directory(
            document_id
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            directory
            / self.DOCUMENT_FILENAME
        )

        path.write_text(
            document.model_dump_json(
                indent=2
            ),
            encoding="utf-8",
        )

    def load_document(
        self,
        document_id: str,
    ) -> StructuredDocument:

        path = (
            self._document_directory(
                document_id
            )
            / self.DOCUMENT_FILENAME
        )

        return (
            StructuredDocument.model_validate_json(
                path.read_text(
                    encoding="utf-8"
                )
            )
        )

    # ---------------------------------------------------------
    # Chunks
    # ---------------------------------------------------------

    def save_chunks(
        self,
        document_id: str,
        chunks: ChunkCollection,
    ) -> None:

        directory = self._document_directory(
            document_id
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            directory
            / self.CHUNKS_FILENAME
        )

        path.write_text(
            chunks.model_dump_json(
                indent=2
            ),
            encoding="utf-8",
        )

    def load_chunks(
        self,
        document_id: str,
    ) -> ChunkCollection:

        path = (
            self._document_directory(
                document_id
            )
            / self.CHUNKS_FILENAME
        )

        return (
            ChunkCollection.model_validate_json(
                path.read_text(
                    encoding="utf-8"
                )
            )
        )

    # ---------------------------------------------------------
    # Vector Store
    # ---------------------------------------------------------

    def save_vector_store(
        self,
        document_id: str,
        vector_store: FAISSVectorStore,
    ) -> None:

        directory = self._document_directory(
            document_id
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        vector_store.save(
            directory
        )

    def load_vector_store(
        self,
        document_id: str,
        vector_store: FAISSVectorStore,
    ) -> None:

        directory = self._document_directory(
            document_id
        )

        vector_store.load_and_merge(
            directory
        )

    # ---------------------------------------------------------
    # BM25 Index
    # ---------------------------------------------------------

    def save_bm25_index(
        self,
        document_id: str,
        bm25_index: BM25Index,
    ) -> None:
        """
        Persist the BM25 index.
        """

        directory = self._document_directory(
            document_id
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        bm25_index.save(
            directory
        )

    def load_bm25_index(
        self,
        document_id: str,
        bm25_index: BM25Index,
    ) -> None:
        """
        Load a persisted BM25 index and merge it into
        the existing in-memory index.
        """

        directory = self._document_directory(
            document_id
        )

        bm25_index.load_and_merge(
            directory
        )