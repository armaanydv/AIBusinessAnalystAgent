from app.retrieval.bm25.bm25_index import BM25Index
from app.retrieval.repository.chunk_repository import (
    ChunkRepository,
)
from app.retrieval.vector_store.faiss_vector_store import (
    FAISSVectorStore,
)
from app.storage.artifact_storage import ArtifactStorage


class KnowledgeBaseService:
    """
    Manages the lifecycle of the Knowledge Base.

    Responsible for restoring persisted documents,
    rebuilding in-memory retrieval components, and
    deleting documents.
    """

    def __init__(
        self,
        artifact_storage: ArtifactStorage,
        chunk_repository: ChunkRepository,
        vector_store: FAISSVectorStore,
        bm25_index: BM25Index,
    ) -> None:

        self._artifact_storage = artifact_storage
        self._chunk_repository = chunk_repository
        self._vector_store = vector_store
        self._bm25_index = bm25_index

    # ---------------------------------------------------------
    # Restore Knowledge Base
    # ---------------------------------------------------------

    def restore(
        self,
    ) -> None:
        """
        Restore all persisted documents into the
        in-memory Knowledge Base.
        """

        for document_id in (
            self._artifact_storage.list_documents()
        ):

            chunks = self._artifact_storage.load_chunks(
                document_id
            )

            self._chunk_repository.add_many(
                chunks
            )

            self._artifact_storage.load_vector_store(
                document_id=document_id,
                vector_store=self._vector_store,
            )

            self._artifact_storage.load_bm25_index(
                document_id=document_id,
                bm25_index=self._bm25_index,
            )

    # ---------------------------------------------------------
    # Rebuild Knowledge Base
    # ---------------------------------------------------------

    def rebuild(
        self,
    ) -> None:
        """
        Clear all in-memory retrieval components and
        restore the Knowledge Base from persisted artifacts.
        """

        self._chunk_repository.clear()

        self._vector_store.clear()

        self._bm25_index.clear()

        self.restore()

    # ---------------------------------------------------------
    # Delete Document
    # ---------------------------------------------------------

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document from persistent storage and
        rebuild the in-memory Knowledge Base.
        """

        if not self._artifact_storage.document_exists(
            document_id
        ):
            raise FileNotFoundError(
                f"Document '{document_id}' does not exist."
            )

        # Delete persisted artifacts
        self._artifact_storage.delete_document(
            document_id
        )

        # Rebuild in-memory Knowledge Base
        self.rebuild()