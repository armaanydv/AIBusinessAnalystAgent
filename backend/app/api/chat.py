from fastapi import APIRouter

from app.api.schemas.chat import (
    ChatRequestSchema,
    ChatResponseSchema,
    LLMUsageSchema,
    RetrievalResultSchema,
)
from app.core.bootstrap import rag_service
from app.rag.rag_request import RAGRequest


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponseSchema,
)
def chat(
    request: ChatRequestSchema,
):
    rag_request = RAGRequest(
        query=request.query,
        top_k=request.top_k,
    )

    response = rag_service.generate(
        request=rag_request,
    )

    return ChatResponseSchema(
        answer=response.answer,
        retrieval_results=[
            RetrievalResultSchema(
                chunk_id=result.chunk.id,
                title=result.chunk.title,
                retrieval_score=result.retrieval_score,
                rerank_score=result.rerank_score,
                text=result.chunk.text,
            )
            for result in response.retrieval_results
        ],
        llm=LLMUsageSchema(
            input_tokens=response.llm_response.input_tokens,
            output_tokens=response.llm_response.output_tokens,
            total_tokens=response.llm_response.total_tokens,
            finish_reason=response.llm_response.finish_reason,
        ),
    )