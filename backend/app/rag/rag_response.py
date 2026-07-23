from dataclasses import dataclass

from app.llm.llm_response import LLMResponse
from app.retrieval.retriever.retrieval_result import RetrievalResult


@dataclass(slots=True, frozen=True)
class RAGResponse:
    """
    Final response returned by the RAG pipeline.
    """

    answer: str
    retrieval_results: list[RetrievalResult]
    llm_response: LLMResponse