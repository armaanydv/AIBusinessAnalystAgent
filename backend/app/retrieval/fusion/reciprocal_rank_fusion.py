from collections import defaultdict

from app.retrieval.fusion.base_fusion import BaseFusion
from app.retrieval.retriever.retrieval_result import RetrievalResult


class ReciprocalRankFusion(BaseFusion):
    """
    Implements the Reciprocal Rank Fusion (RRF) algorithm.

    Reference:
        Cormack et al. (2009)
        Reciprocal Rank Fusion Outperforms Condorcet and
        Individual Rank Learning Methods.
    """

    def __init__(
        self,
        rrf_k: int = 60,
    ) -> None:
        self._rrf_k = rrf_k

    def fuse(
        self,
        result_sets: list[list[RetrievalResult]],
        k: int,
    ) -> list[RetrievalResult]:

        scores: dict[str, float] = defaultdict(float)

        chunk_lookup: dict[str, RetrievalResult] = {}

        for result_set in result_sets:

            for result in result_set:

                chunk_id = result.chunk.id

                scores[chunk_id] += (
                    1.0 / (self._rrf_k + result.rank)
                )

                chunk_lookup[chunk_id] = result

        fused_results = sorted(
            chunk_lookup.values(),
            key=lambda result: scores[result.chunk.id],
            reverse=True,
        )

        final_results: list[RetrievalResult] = []

        for rank, result in enumerate(
            fused_results[:k],
            start=1,
        ):

            final_results.append(
                RetrievalResult(
                    chunk=result.chunk,
                    similarity_score=scores[result.chunk.id],
                    rank=rank,
                )
            )

        return final_results