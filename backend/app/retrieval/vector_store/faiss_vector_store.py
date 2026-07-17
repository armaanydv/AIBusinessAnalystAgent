import logging
import pickle
from pathlib import Path

import faiss
import numpy as np

from app.retrieval.vector_store.base_vector_store import BaseVectorStore
from app.retrieval.vector_store.vector_record import VectorRecord

logger = logging.getLogger(__name__)


class FAISSVectorStore(BaseVectorStore):
    """
    FAISS implementation of a vector store.

    Uses cosine similarity by storing normalized vectors
    in an IndexFlatIP (Inner Product) index.
    """

    INDEX_FILENAME = "vector.index"
    MAPPING_FILENAME = "mapping.pkl"

    def __init__(
        self,
        dimension: int,
    ) -> None:

        self.dimension = dimension

        # Cosine similarity using normalized vectors
        self.index = faiss.IndexFlatIP(dimension)

        # FAISS index -> chunk id
        self.index_to_chunk: dict[int, str] = {}

    # ---------------------------------------------------------
    # Add
    # ---------------------------------------------------------

    def add(
        self,
        record: VectorRecord,
    ) -> None:

        vector = np.asarray(
            record.vector,
            dtype=np.float32,
        ).reshape(1, -1)

        if vector.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"received {vector.shape[1]}."
            )

        faiss.normalize_L2(vector)

        current_index = self.index.ntotal

        self.index.add(vector)

        self.index_to_chunk[current_index] = record.chunk_id

        logger.debug(
            "Indexed chunk '%s'.",
            record.chunk_id,
        )

    # ---------------------------------------------------------
    # Batch Add
    # ---------------------------------------------------------

    def add_many(
        self,
        records: list[VectorRecord],
    ) -> None:

        if not records:
            return

        vectors = np.asarray(
            [record.vector for record in records],
            dtype=np.float32,
        )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"received {vectors.shape[1]}."
            )

        faiss.normalize_L2(vectors)

        start_index = self.index.ntotal

        self.index.add(vectors)

        for offset, record in enumerate(records):

            self.index_to_chunk[
                start_index + offset
            ] = record.chunk_id

        logger.info(
            "Indexed %d vectors.",
            len(records),
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[tuple[str, float]]:

        if self.index.ntotal == 0:
            return []

        vector = np.asarray(
            query_vector,
            dtype=np.float32,
        ).reshape(1, -1)

        if vector.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"received {vector.shape[1]}."
            )

        faiss.normalize_L2(vector)

        scores, indices = self.index.search(
            vector,
            min(k, self.index.ntotal),
        )

        results: list[tuple[str, float]] = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            chunk_id = self.index_to_chunk.get(index)

            if chunk_id is None:
                continue

            results.append(
                (
                    chunk_id,
                    float(score),
                )
            )

        return results

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(
        self,
        directory: str | Path,
    ) -> None:

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(
                directory / self.INDEX_FILENAME
            ),
        )

        with open(
            directory / self.MAPPING_FILENAME,
            "wb",
        ) as file:

            pickle.dump(
                self.index_to_chunk,
                file,
            )

        logger.info(
            "Vector store saved to '%s'.",
            directory,
        )

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load(
        self,
        directory: str | Path,
    ) -> None:

        directory = Path(directory)

        self.index = faiss.read_index(
            str(
                directory / self.INDEX_FILENAME
            )
        )

        with open(
            directory / self.MAPPING_FILENAME,
            "rb",
        ) as file:

            self.index_to_chunk = pickle.load(
                file
            )

        logger.info(
            "Vector store loaded from '%s'.",
            directory,
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def size(
        self,
    ) -> int:

        return self.index.ntotal

    def __len__(
        self,
    ) -> int:

        return self.size

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"size={self.size}, "
            f"dimension={self.dimension})"
        )