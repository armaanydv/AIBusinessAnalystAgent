from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest
from app.prompting.base_prompt_builder import BasePromptBuilder
from app.rag.rag_request import RAGRequest
from app.rag.rag_response import RAGResponse
from app.retrieval.retriever.base_retriever import BaseRetriever


class RAGService:
    """
    Orchestrates the complete Retrieval-Augmented Generation pipeline.

    Pipeline:
        Query
            ↓
        Retriever
            ↓
        Prompt Builder
            ↓
        LLM
            ↓
        RAG Response
    """

    def __init__(
        self,
        retriever: BaseRetriever,
        prompt_builder: BasePromptBuilder,
        llm: BaseLLM,
    ) -> None:
        self._retriever = retriever
        self._prompt_builder = prompt_builder
        self._llm = llm

    def generate(
        self,
        request: RAGRequest,
    ) -> RAGResponse:
        """
        Generate an answer for a user query using Retrieval-Augmented Generation.
        """

        retrieval_results = self._retriever.retrieve(
            query=request.query,
            k=request.top_k,
        )

        prompt = self._prompt_builder.build(
            query=request.query,
            retrieval_results=retrieval_results,
        )

        llm_response = self._llm.generate(
            LLMRequest(prompt=prompt)
        )

        return RAGResponse(
            answer=llm_response.content,
            retrieval_results=retrieval_results,
            llm_response=llm_response,
        )