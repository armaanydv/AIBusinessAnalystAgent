from pydantic import BaseModel, Field


class ChatRequestSchema(BaseModel):
    """
    Request body for the chat API.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to answer using the document knowledge base.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of document chunks to retrieve.",
    )


class RetrievalResultSchema(BaseModel):
    """
    A retrieved document chunk returned as supporting context.
    """

    chunk_id: str

    title: str | None

    retrieval_score: float | None

    rerank_score: float | None

    text: str


class LLMUsageSchema(BaseModel):
    """
    LLM usage information for the request.
    """

    input_tokens: int | None

    output_tokens: int | None

    total_tokens: int | None

    finish_reason: str | None


class ChatResponseSchema(BaseModel):
    """
    Response returned by the chat API.
    """

    answer: str

    retrieval_results: list[RetrievalResultSchema]

    llm: LLMUsageSchema