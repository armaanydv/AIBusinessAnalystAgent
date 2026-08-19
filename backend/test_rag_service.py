from app.rag.rag_request import RAGRequest
from app.retrieval.retriever.retrieval_result import RetrievalResult
from app.services.rag_service import RAGService


class FakeRetriever:
    def retrieve(self, query: str, k: int = 5):
        return [
            RetrievalResult(
                chunk="chunk 1",
                similarity_score=0.8,
                rank=1,
            ),
            RetrievalResult(
                chunk="chunk 2",
                similarity_score=0.7,
                rank=2,
            ),
        ]


class FakeReranker:
    def rerank(self, query: str, retrieval_results):
        return retrieval_results


class FakePromptBuilder:
    def build(self, query: str, retrieval_results):
        return "fake prompt"


class FakeLLM:
    def generate(self, request):
        raise AssertionError(
            "LLM should not be called by RAGService.retrieve()"
        )


class FakeOutputParser:
    pass


def test_rag_service_retrieve_returns_reranked_results():
    service = RAGService(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        prompt_builder=FakePromptBuilder(),
        llm=FakeLLM(),
        output_parser=FakeOutputParser(),
    )

    request = RAGRequest(
        query="revenue by product in North region",
        top_k=5,
    )

    results = service.retrieve(request)

    assert len(results) == 2
    assert results[0].chunk == "chunk 1"
    assert results[1].chunk == "chunk 2"
    assert results[0].similarity_score == 0.8
    assert results[1].similarity_score == 0.7


def test_rag_service_retrieve_uses_request_query_and_top_k():
    class TrackingRetriever:
        def __init__(self):
            self.query = None
            self.k = None

        def retrieve(self, query: str, k: int = 5):
            self.query = query
            self.k = k
            return []

    retriever = TrackingRetriever()

    service = RAGService(
        retriever=retriever,
        reranker=FakeReranker(),
        prompt_builder=FakePromptBuilder(),
        llm=FakeLLM(),
        output_parser=FakeOutputParser(),
    )

    request = RAGRequest(
        query="revenue by product",
        top_k=10,
    )

    service.retrieve(request)

    assert retriever.query == "revenue by product"
    assert retriever.k == 10