import logging

from app.retrieval.embeddings.base_embedding_model import BaseEmbeddingModel
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult
from app.retrieval.vector_store.base_vector_store import BaseVectorStore
from app.retrieval.repository.chunk_repository import ChunkRepository

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
    chunk_repository: ChunkRepository,
) -> None:

       self.embedding_model = embedding_model
       self.vector_store = vector_store
       self._chunk_repository = chunk_repository

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k most relevant chunks.
        """

        if len(self._chunk_repository) == 0:
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

        for rank, (chunk_id, score) in enumerate(
            matches,
            start=1,
        ):

            chunk = self._chunk_repository.get(chunk_id)

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
                    rank=rank,
                )
            )

        return results