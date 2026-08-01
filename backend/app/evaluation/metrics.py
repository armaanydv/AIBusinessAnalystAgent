"""
Evaluation metrics for the retrieval benchmarking framework.

This module contains pure metric functions used to evaluate
retrieval performance. These functions are deterministic,
stateless, and independent of the retrieval implementation.
"""

from __future__ import annotations

from statistics import mean
from app.retrieval.retriever.retrieval_result import RetrievalResult


def calculate_recall_at_k(
    expected_chunk_ids: list[str],
    retrieved_results: list[RetrievalResult],
    k: int,
) -> float:
    """
    Calculate Recall@K.

    Recall@K measures the fraction of relevant chunks
    that were retrieved within the top K results.
    """

    if not expected_chunk_ids:
        return 0.0

    expected = set(expected_chunk_ids)

    retrieved = {
        result.chunk.id
        for result in retrieved_results[:k]
    }

    relevant = expected.intersection(retrieved)

    return len(relevant) / len(expected)


def calculate_precision_at_k(
    expected_chunk_ids: list[str],
    retrieved_results: list[RetrievalResult],
    k: int,
) -> float:
    """
    Calculate Precision@K.

    Precision@K measures the fraction of the top K retrieved
    results that are relevant.
    """

    if k <= 0:
        return 0.0

    retrieved = retrieved_results[:k]

    if not retrieved:
        return 0.0

    expected = set(expected_chunk_ids)

    relevant = sum(
        result.chunk.id in expected
        for result in retrieved
    )

    return relevant / len(retrieved)


def calculate_reciprocal_rank(
    expected_chunk_ids: list[str],
    retrieved_results: list[RetrievalResult],
) -> float:
    """
    Calculate Reciprocal Rank (RR).

    RR = 1 / rank of the first relevant result.

    Returns 0.0 if no relevant result is found.
    """

    expected = set(expected_chunk_ids)

    for index, result in enumerate(retrieved_results, start=1):
        if result.chunk.id in expected:
            return 1.0 / index

    return 0.0


def calculate_hit_rate(
    expected_chunk_ids: list[str],
    retrieved_results: list[RetrievalResult],
    k: int,
) -> float:
    """
    Calculate Hit Rate@K.

    Returns:

        1.0 if at least one relevant result is retrieved.

        0.0 otherwise.
    """

    expected = set(expected_chunk_ids)

    for result in retrieved_results[:k]:
        if result.chunk.id in expected:
            return 1.0

    return 0.0


def calculate_average_latency(
    latencies_ms: list[float],
) -> float:
    """
    Calculate average retrieval latency.
    """

    if not latencies_ms:
        return 0.0

    return mean(latencies_ms)


def calculate_average_similarity(
    retrieved_results: list[RetrievalResult],
) -> float:
    """
    Calculate the average similarity score
    of retrieved results.
    """

    if not retrieved_results:
        return 0.0

    return mean(
        result.score
        for result in retrieved_results
    )