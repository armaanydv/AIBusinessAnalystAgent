from app.retrieval.retriever.base_retriever import BaseRetriever
from app.retrieval.retriever.retrieval_result import RetrievalResult


class RetrievalService:
    """
    Service responsible for retrieving the most relevant
    document chunks for a user query.

    This layer hides the retrieval implementation from
    the API and future RAG pipeline.
    """

    def __init__(
        self,
        retriever: BaseRetriever,
    ) -> None:
        self._retriever = retriever

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the top-k most relevant chunks.

        Args:
            query:
                User's natural language query.

            k:
                Number of chunks to retrieve.

        Returns:
            Ranked retrieval results.
        """

        return self._retriever.retrieve(
            query=query,
            k=k,
        )