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
        Updates the retriever with the latest document chunks.
        """

        self.chunk_lookup = {
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

        for rank, (chunk_id, score) in enumerate(matches, start=1):
          ...
          results.append(
          RetrievalResult(
            chunk=chunk,
            similarity_score=score,
            rank=rank,
        )
    )

        return results