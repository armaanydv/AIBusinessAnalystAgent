from __future__ import annotations

from rank_bm25 import BM25Okapi

from app.document.chunking.chunk_collection import ChunkCollection
from app.retrieval.bm25.bm25_config import BM25Config
from app.retrieval.bm25.tokenizer import BM25Tokenizer


class BM25Index:
    """
    BM25 lexical search index.

    Wraps the rank_bm25 implementation and exposes
    a clean interface for building and searching
    the index.
    """

    def __init__(
        self,
        tokenizer: BM25Tokenizer,
        config: BM25Config | None = None,
    ) -> None:

        self._tokenizer = tokenizer
        self._config = config or BM25Config()

        self._index: BM25Okapi | None = None

        self._chunk_ids: list[str] = []

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(
        self,
        chunks: ChunkCollection,
    ) -> None:
        """
        Build the BM25 index from a collection of chunks.
        """

        corpus = []

        self._chunk_ids.clear()

        for chunk in chunks.chunks:

            corpus.append(
                self._tokenizer.tokenize(
                    chunk.text
                )
            )

            self._chunk_ids.append(
                chunk.id
            )

        self._index = BM25Okapi(
            corpus=corpus,
            k1=self._config.k1,
            b=self._config.b,
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[tuple[str, float]]:
        """
        Search the BM25 index.

        Returns:
            List of (chunk_id, score) pairs sorted by
            descending BM25 score.
        """

        if self._index is None:
            return []

        query_tokens = self._tokenizer.tokenize(
            query
        )

        scores = self._index.get_scores(
            query_tokens
        )

        ranked = sorted(
            zip(
                self._chunk_ids,
                scores,
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            (
                chunk_id,
                float(score),
            )
            for chunk_id, score in ranked[:k]
        ]

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def size(
        self,
    ) -> int:
        """
        Number of indexed chunks.
        """

        return len(
            self._chunk_ids
        )