import logging

from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection
from app.retrieval.embeddings.base_embedding_model import BaseEmbeddingModel
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult
from app.retrieval.vector_store.base_vector_store import BaseVectorStore

logger = logging.getLogger(__name__)


class SemanticRetriever(BaseRetriever):
    """
    Retrieves the most semantically similar chunks using
    vector similarity search.
    """

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
        vector_store: BaseVectorStore,
    ) -> None:

        self.embedding_model = embedding_model
        self.vector_store = vector_store

        self.chunk_lookup: dict[str, Chunk] = {}

    def set_chunks(
        self,
        chunks: ChunkCollection,
    ) -> None:
        """
        Adds document chunks to the retriever.

        Existing chunks are preserved so multiple documents
        can be searched simultaneously.
        """

        for chunk in chunks.chunks:
            self.chunk_lookup[chunk.id] = chunk

        logger.info(
            "Loaded %d chunks. Total chunks: %d",
            len(chunks.chunks),
            len(self.chunk_lookup),
        )

    def clear_chunks(
        self,
    ) -> None:
        """
        Clears all loaded chunks.
        """

        self.chunk_lookup.clear()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k most relevant chunks.
        """

        if not self.chunk_lookup:
            logger.warning(
                "Retriever has no chunks loaded."
            )
            return []

        query_vector = self.embedding_model.encode(
            [query]
        )[0]

        matches = self.vector_store.search(
            query_vector=query_vector,
            k=k,
        )

        results: list[RetrievalResult] = []

        for chunk_id, score in matches:

            chunk = self.chunk_lookup.get(chunk_id)

            if chunk is None:
                logger.warning(
                    "Chunk '%s' not found.",
                    chunk_id,
                )
                continue

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    similarity_score=score,
                )
            )

        return results