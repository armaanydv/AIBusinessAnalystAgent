import logging

from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection
from app.retrieval.bm25.bm25_index import BM25Index
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
        bm25_index: BM25Index,
    ) -> None:

        self._bm25_index = bm25_index
        self._chunk_lookup: dict[str, Chunk] = {}

    def set_chunks(
        self,
        chunks: ChunkCollection,
    ) -> None:
        """
        Build the BM25 index and load chunks.
        """

        self._bm25_index.build(chunks)

        self._chunk_lookup = {
            chunk.id: chunk
            for chunk in chunks.chunks
        }

        logger.info(
            "Loaded %d chunks into BM25.",
            len(chunks.chunks),
        )

    def clear_chunks(
        self,
    ) -> None:
        """
        Clear the retriever.
        """

        self._chunk_lookup.clear()
        self._bm25_index.clear()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k BM25 matches.
        """

        if not self._chunk_lookup:

            logger.warning(
                "BM25 retriever has no chunks loaded."
            )

            return []

        matches = self._bm25_index.search(
            query=query,
            k=k,
        )

        results: list[RetrievalResult] = []

        for rank, (chunk_id, score) in enumerate(
            matches,
            start=1,
        ):

            chunk = self._chunk_lookup.get(
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