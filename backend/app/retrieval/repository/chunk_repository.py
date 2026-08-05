from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection


class ChunkRepository:
    """
    In-memory repository for document chunks.

    Acts as the single source of truth for all chunks used
    throughout the retrieval pipeline.
    """

    def __init__(self) -> None:

        self._chunks: dict[str, Chunk] = {}

    def add(
        self,
        chunk: Chunk,
    ) -> None:
        """
        Add or update a chunk.
        """

        self._chunks[chunk.id] = chunk

    def add_many(
        self,
        chunks: ChunkCollection,
    ) -> None:
        """
        Add multiple chunks.
        """

        for chunk in chunks.chunks:
            self.add(chunk)

    def get(
        self,
        chunk_id: str,
    ) -> Chunk | None:
        """
        Retrieve a chunk by its id.
        """

        return self._chunks.get(chunk_id)

    def remove(
        self,
        chunk_id: str,
    ) -> None:
        """
        Remove a chunk.
        """

        self._chunks.pop(chunk_id, None)

    def clear(self) -> None:
        """
        Remove all chunks.
        """

        self._chunks.clear()

    def __contains__(
        self,
        chunk_id: str,
    ) -> bool:

        return chunk_id in self._chunks

    def __len__(self) -> int:

        return len(self._chunks)