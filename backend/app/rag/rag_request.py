from pydantic import BaseModel


class RAGRequest(BaseModel):
    """
    Represents a user request to the RAG pipeline.
    """

    query: str
    top_k: int = 5