"""
Retrieval-Augmented Generation service.
"""

from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest
from app.llm.output_parser import OutputParser
from app.outputs.rag_answer import RAGAnswer
from app.prompting.base_prompt_builder import BasePromptBuilder
from app.rag.rag_request import RAGRequest
from app.rag.rag_response import RAGResponse
from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult
from app.retrieval.reranker.base_reranker import BaseReranker


class RAGService:
    """
    Orchestrates the Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        prompt_builder: BasePromptBuilder,
        llm: BaseLLM,
        output_parser: OutputParser,
    ) -> None:
        self._retriever = retriever
        self._reranker = reranker
        self._prompt_builder = prompt_builder
        self._llm = llm
        self._output_parser = output_parser

    def retrieve(
        self,
        request: RAGRequest,
    ) -> list[RetrievalResult]:
        """
        Retrieve and rerank relevant document chunks.
        """

        retrieval_results = self._retriever.retrieve(
            query=request.query,
            k=request.top_k,
        )

        return self._reranker.rerank(
            query=request.query,
            retrieval_results=retrieval_results,
        )

    def generate(
        self,
        request: RAGRequest,
    ) -> RAGResponse:
        """
        Generate an answer using Retrieval-Augmented Generation.
        """

        reranked_results = self.retrieve(request)

        prompt = self._prompt_builder.build(
            query=request.query,
            retrieval_results=reranked_results,
        )

        llm_response = self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        parsed_output = self._output_parser.parse(
            llm_response,
            RAGAnswer,
        )

        return RAGResponse(
            answer=parsed_output.answer,
            retrieval_results=reranked_results,
            llm_response=llm_response,
        )