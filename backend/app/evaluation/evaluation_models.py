"""
Pydantic models for the evaluation and benchmarking module.

These models define the data structures used to benchmark
the retrieval performance of the RAG pipeline.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.retrieval.retriever.retrieval_result import RetrievalResult


class BenchmarkQuestion(BaseModel):
    """
    Represents a single benchmark question.

    Each benchmark question contains the expected chunk(s)
    that should be retrieved by the retrieval engine.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        ...,
        description="Unique identifier for the benchmark question.",
    )

    question: str = Field(
        ...,
        description="Natural language query used for retrieval evaluation.",
    )

    expected_chunk_ids: list[str] = Field(
        ...,
        description="Expected chunk IDs that should be retrieved.",
    )

    expected_document: str | None = Field(
        default=None,
        description="Expected source document.",
    )

    category: str | None = Field(
        default=None,
        description="Benchmark category (financial, legal, operations, etc.).",
    )

    difficulty: Literal["easy", "medium", "hard"] | None = Field(
        default=None,
        description="Difficulty level of the benchmark question.",
    )


class QuestionEvaluation(BaseModel):
    """
    Stores the evaluation result for a single benchmark question.
    """

    model_config = ConfigDict(extra="forbid")

    question: BenchmarkQuestion = Field(
        ...,
        description="Benchmark question being evaluated.",
    )

    retrieved_results: list[RetrievalResult] = Field(
        default_factory=list,
        description="Results returned by the retrieval pipeline.",
    )

    recall_at_1: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Recall@1 score.",
    )

    recall_at_5: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Recall@5 score.",
    )

    precision_at_5: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Precision@5 score.",
    )

    reciprocal_rank: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Reciprocal Rank (RR).",
    )

    hit: bool = Field(
        ...,
        description="Whether at least one relevant result was retrieved.",
    )

    latency_ms: float = Field(
        ...,
        ge=0.0,
        description="Retrieval latency in milliseconds.",
    )


class BenchmarkReport(BaseModel):
    """
    Represents the aggregated benchmark report for an evaluation run.
    """

    model_config = ConfigDict(extra="forbid")

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the benchmark completed.",
    )

    total_questions: int = Field(
        ...,
        ge=0,
        description="Total number of benchmark questions evaluated.",
    )

    recall_at_1: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall Recall@1.",
    )

    recall_at_5: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall Recall@5.",
    )

    precision_at_5: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall Precision@5.",
    )

    mrr: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Mean Reciprocal Rank (MRR).",
    )

    hit_rate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall Hit Rate.",
    )

    average_latency_ms: float = Field(
        ...,
        ge=0.0,
        description="Average retrieval latency in milliseconds.",
    )

    evaluations: list[QuestionEvaluation] = Field(
        default_factory=list,
        description="Per-question evaluation results.",
    )