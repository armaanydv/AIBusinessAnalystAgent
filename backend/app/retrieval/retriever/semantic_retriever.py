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
        chunks: ChunkCollection,
    ) -> None:

        self.embedding_model = embedding_model
        self.vector_store = vector_store

        self.chunk_lookup: dict[str, Chunk] = {
            chunk.id: chunk
            for chunk in chunks.chunks
        }

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k most relevant chunks.
        """

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