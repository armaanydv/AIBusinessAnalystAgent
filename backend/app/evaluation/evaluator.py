"""
Core retrieval evaluation engine.
"""

from __future__ import annotations

import logging
from time import perf_counter

from app.evaluation.evaluation_models import (
    BenchmarkQuestion,
    BenchmarkReport,
    QuestionEvaluation,
)
from app.evaluation.metrics import (
    calculate_average_latency,
    calculate_hit_rate,
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_reciprocal_rank,
)
from app.retrieval.retriever.base_retriever import BaseRetriever

logger = logging.getLogger(__name__)


class RetrievalEvaluator:
    """
    Evaluates a retriever against a benchmark dataset.
    """

    RECALL_AT_1 = 1
    RECALL_AT_5 = 5
    PRECISION_AT_5 = 5
    MINIMUM_RETRIEVAL_K = 5

    def __init__(
        self,
        retriever: BaseRetriever,
        retrieval_k: int = 5,
    ) -> None:
        """
        Initialize the evaluator.

        Args:
            retriever:
                Retriever implementation to benchmark.

            retrieval_k:
                Number of results retrieved per query.
                Must be at least 5 because Recall@5 and
                Precision@5 are computed.
        """

        if retrieval_k < self.MINIMUM_RETRIEVAL_K:
            raise ValueError(
                f"retrieval_k must be at least "
                f"{self.MINIMUM_RETRIEVAL_K}."
            )

        self._retriever = retriever
        self._retrieval_k = retrieval_k

    def evaluate(
        self,
        benchmark_questions: list[BenchmarkQuestion],
    ) -> BenchmarkReport:
        """
        Evaluate an entire benchmark dataset.
        """

        logger.info(
            "Starting retrieval benchmark "
            "with %d questions.",
            len(benchmark_questions),
        )

        evaluations: list[QuestionEvaluation] = []

        total_questions = len(
            benchmark_questions
        )

        for index, question in enumerate(
            benchmark_questions,
            start=1,
        ):

            logger.info(
                "Evaluating question %d/%d (%s)",
                index,
                total_questions,
                question.id,
            )

            try:

                evaluations.append(
                    self._evaluate_question(
                        question
                    )
                )

            except Exception:

                logger.exception(
                    "Failed to evaluate "
                    "question '%s'.",
                    question.id,
                )

        if not evaluations:

            logger.warning(
                "No benchmark questions "
                "were successfully evaluated."
            )

            return BenchmarkReport(
                total_questions=0,
                recall_at_1=0.0,
                recall_at_5=0.0,
                precision_at_5=0.0,
                mrr=0.0,
                hit_rate=0.0,
                average_latency_ms=0.0,
                evaluations=[],
            )

        logger.info(
            "Benchmark completed successfully."
        )

        return BenchmarkReport(
            total_questions=len(evaluations),
            recall_at_1=self._average(
                [
                    evaluation.recall_at_1
                    for evaluation in evaluations
                ]
            ),
            recall_at_5=self._average(
                [
                    evaluation.recall_at_5
                    for evaluation in evaluations
                ]
            ),
            precision_at_5=self._average(
                [
                    evaluation.precision_at_5
                    for evaluation in evaluations
                ]
            ),
            mrr=self._average(
                [
                    evaluation.reciprocal_rank
                    for evaluation in evaluations
                ]
            ),
            hit_rate=self._average(
                [
                    float(evaluation.hit)
                    for evaluation in evaluations
                ]
            ),
            average_latency_ms=calculate_average_latency(
                [
                    evaluation.latency_ms
                    for evaluation in evaluations
                ]
            ),
            evaluations=evaluations,
        )

    def _evaluate_question(
        self,
        question: BenchmarkQuestion,
    ) -> QuestionEvaluation:
        """
        Evaluate a single benchmark question.
        """

        start = perf_counter()

        results = self._retriever.retrieve(
            query=question.question,
            k=self._retrieval_k,
        )

        latency_ms = (
            perf_counter() - start
        ) * 1000

        return QuestionEvaluation(
            question=question,
            retrieved_results=results,
            recall_at_1=calculate_recall_at_k(
                question.expected_chunk_ids,
                results,
                self.RECALL_AT_1,
            ),
            recall_at_5=calculate_recall_at_k(
                question.expected_chunk_ids,
                results,
                self.RECALL_AT_5,
            ),
            precision_at_5=calculate_precision_at_k(
                question.expected_chunk_ids,
                results,
                self.PRECISION_AT_5,
            ),
            reciprocal_rank=calculate_reciprocal_rank(
                question.expected_chunk_ids,
                results,
            ),
            hit=bool(
                calculate_hit_rate(
                    question.expected_chunk_ids,
                    results,
                    self.RECALL_AT_5,
                )
            ),
            latency_ms=latency_ms,
        )

    @staticmethod
    def _average(
        values: list[float],
    ) -> float:
        """
        Compute the arithmetic mean of a list.

        Returns 0.0 for an empty list.
        """

        if not values:
            return 0.0

        return sum(values) / len(values)