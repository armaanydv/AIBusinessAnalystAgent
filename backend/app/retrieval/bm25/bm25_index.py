from __future__ import annotations

from pathlib import Path

from rank_bm25 import BM25Okapi

from app.document.chunking.chunk_collection import ChunkCollection
from app.retrieval.bm25.bm25_config import BM25Config
from app.retrieval.bm25.bm25_index_artifact import BM25IndexArtifact
from app.retrieval.bm25.tokenizer import BM25Tokenizer


class BM25Index:
    """
    BM25 lexical search index.

    Wraps rank_bm25 and provides a clean interface for
    building, searching, saving, loading and clearing
    the index.
    """

    INDEX_FILENAME = "bm25_index.json"

    def __init__(
        self,
        tokenizer: BM25Tokenizer,
        config: BM25Config | None = None,
    ) -> None:

        self._tokenizer = tokenizer
        self._config = config or BM25Config()

        self._index: BM25Okapi | None = None

        self._chunk_ids: list[str] = []
        self._tokenized_corpus: list[list[str]] = []

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(
        self,
        chunks: ChunkCollection,
    ) -> None:
        """
        Build the BM25 index from document chunks.
        """

        self.clear()

        for chunk in chunks.chunks:

            self._chunk_ids.append(
                chunk.id
            )

            self._tokenized_corpus.append(
                self._tokenizer.tokenize(
                    chunk.text
                )
            )

        self._index = BM25Okapi(
            corpus=self._tokenized_corpus,
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
    # Persistence
    # ---------------------------------------------------------

    def save(
        self,
        directory: Path,
    ) -> None:
        """
        Persist the BM25 index.
        """

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact = BM25IndexArtifact(
            chunk_ids=self._chunk_ids,
            tokenized_corpus=self._tokenized_corpus,
        )

        path = (
            directory
            / self.INDEX_FILENAME
        )

        path.write_text(
            artifact.model_dump_json(
                indent=2,
            ),
            encoding="utf-8",
        )

    def load(
        self,
        directory: Path,
    ) -> None:
        """
        Load a persisted BM25 index.
        """

        path = (
            directory
            / self.INDEX_FILENAME
        )

        artifact = (
            BM25IndexArtifact.model_validate_json(
                path.read_text(
                    encoding="utf-8",
                )
            )
        )

        self._chunk_ids = artifact.chunk_ids
        self._tokenized_corpus = (
            artifact.tokenized_corpus
        )

        self._index = BM25Okapi(
            corpus=self._tokenized_corpus,
            k1=self._config.k1,
            b=self._config.b,
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Clear the loaded BM25 index.
        """

        self._index = None
        self._chunk_ids.clear()
        self._tokenized_corpus.clear()

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