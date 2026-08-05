import logging

from app.retrieval.bm25.bm25_index import BM25Index
from app.retrieval.repository.chunk_repository import ChunkRepository
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult

logger = logging.getLogger(__name__)


class BM25Retriever(BaseRetriever):
    """
    Retrieves the most relevant chunks using
    BM25 lexical search.
    """

    def __init__(
        self,
        index: BM25Index,
        chunk_repository: ChunkRepository,
    ) -> None:

        self._index = index
        self._chunk_repository = chunk_repository

    def clear(
        self,
    ) -> None:
        """
        Clear the BM25 index.
        """

        self._index.clear()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k BM25 matches.
        """

        if len(self._chunk_repository) == 0:

            logger.warning(
                "BM25 retriever has no chunks loaded."
            )

            return []

        matches = self._index.search(
            query=query,
            k=k,
        )

        results: list[RetrievalResult] = []

        for rank, (chunk_id, score) in enumerate(
            matches,
            start=1,
        ):

            chunk = self._chunk_repository.get(
                chunk_id
            )

            if chunk is None:

                logger.warning(
                    "Chunk '%s' not found.",
                    chunk_id,
                )

                continue

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    similarity_score=float(score),
                    rank=rank,
                )
            )

        return results