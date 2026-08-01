from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_metadata import ChunkMetadata
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult


class DummyRetriever(BaseRetriever):
    """
    Dummy retriever used for testing the evaluation module.
    """

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:

        results = []

        for i in range(1, k + 1):

            chunk = Chunk(
                id=f"chunk_{i}",
                text=f"Dummy chunk {i}",
                metadata=ChunkMetadata(
                    source_document="dummy.pdf",
                    start_page=1,
                    end_page=1,
                    hierarchy_level=1,
                ),
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    similarity_score=1.0 / i,
                    rank=i,
                )
            )

        return results