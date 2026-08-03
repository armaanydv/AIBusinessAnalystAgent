import traceback

from fastapi import APIRouter, HTTPException

from app.core.bootstrap import rag_service
from app.rag.rag_request import RAGRequest

router = APIRouter()


@router.post("/chat")
def chat(
    request: RAGRequest,
):
    try:

        response = rag_service.generate(
            request=request,
        )

        return {
            "answer": response.answer,
            "retrieval_results": [
                {
                    "chunk_id": result.chunk.id,
                    "title": result.chunk.title,
                    "similarity_score": result.similarity_score,
                    "text": result.chunk.text,
                }
                for result in response.retrieval_results
            ],
            "llm": {
                "input_tokens": response.llm_response.input_tokens,
                "output_tokens": response.llm_response.output_tokens,
                "total_tokens": response.llm_response.total_tokens,
                "finish_reason": response.llm_response.finish_reason,
            },
        }

    except Exception as exc:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc