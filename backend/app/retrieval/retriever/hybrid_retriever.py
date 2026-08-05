from app.retrieval.fusion.base_fusion import BaseFusion
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.bm25_retriever import BM25Retriever
from app.retrieval.retriever.retrieval_result import RetrievalResult
from app.retrieval.retriever.semantic_retriever import SemanticRetriever


class HybridRetriever(BaseRetriever):
    """
    Hybrid retriever combining semantic and BM25 retrieval
    using a configurable fusion strategy.
    """

    def __init__(
        self,
        semantic_retriever: SemanticRetriever,
        bm25_retriever: BM25Retriever,
        fusion: BaseFusion,
    ) -> None:

        self._semantic_retriever = semantic_retriever
        self._bm25_retriever = bm25_retriever
        self._fusion = fusion

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant chunks using both retrievers and
        fuse the ranked results.
        """

        semantic_results = self._semantic_retriever.retrieve(
            query=query,
            k=k,
        )

        bm25_results = self._bm25_retriever.retrieve(
            query=query,
            k=k,
        )

        return self._fusion.fuse(
            result_sets=[
                semantic_results,
                bm25_results,
            ],
            k=k,
        )