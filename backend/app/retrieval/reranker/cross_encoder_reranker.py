from sentence_transformers import CrossEncoder

from app.retrieval.reranker.base_reranker import (
    BaseReranker,
)
from app.retrieval.reranker.rerank_config import (
    RerankerConfig,
)
from app.retrieval.reranker.rerank_result import (
    RerankResult,
)
from app.retrieval.retriever.retrieval_result import (
    RetrievalResult,
)


class CrossEncoderReranker(BaseReranker):
    """
    Reranks retrieval results using a Hugging Face CrossEncoder model.
    """

    def __init__(
        self,
        config: RerankerConfig,
    ) -> None:

        self._config = config

        self._model = CrossEncoder(
            model_name_or_path=config.model,
        )

    def rerank(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
        k: int | None = None,
    ) -> list[RerankResult]:
        """
        Rerank retrieved chunks using a CrossEncoder.

        Args:
            query:
                User query.

            retrieval_results:
                Results returned by the retriever.

            k:
                Number of reranked results to return.

        Returns:
            Top-k reranked results.
        """

        if not retrieval_results:
            return []

        if k is None:
            k = self._config.top_k

        # ---------------------------------------------------------
        # Build (query, chunk) pairs
        # ---------------------------------------------------------

        sentence_pairs = [
            (
                query,
                result.chunk.text,
            )
            for result in retrieval_results
        ]

        # ---------------------------------------------------------
        # Predict relevance scores
        # ---------------------------------------------------------

        scores = self._model.predict(
            sentence_pairs,
            batch_size=self._config.batch_size,
        )

        # ---------------------------------------------------------
        # Build rerank results
        # ---------------------------------------------------------

        reranked_results = [
            RerankResult(
                chunk=result.chunk,
                retrieval_score=result.similarity_score,
                rerank_score=float(score),
                rank=0,
            )
            for result, score in zip(
                retrieval_results,
                scores,
            )
        ]

        # ---------------------------------------------------------
        # Sort by rerank score
        # ---------------------------------------------------------

        reranked_results.sort(
            key=lambda result: result.rerank_score,
            reverse=True,
        )

        # ---------------------------------------------------------
        # Assign final ranks
        # ---------------------------------------------------------

        final_results = [
            RerankResult(
                chunk=result.chunk,
                retrieval_score=result.retrieval_score,
                rerank_score=result.rerank_score,
                rank=rank,
            )
            for rank, result in enumerate(
                reranked_results[:k],
                start=1,
            )
        ]

        return final_results