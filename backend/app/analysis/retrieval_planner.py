from app.analysis.analysis_request import AnalysisRequest
from app.rag.rag_request import RAGRequest


class RetrievalPlanner:
    def plan(self, analysis_request: AnalysisRequest) -> RAGRequest:
        query_parts = []

        if analysis_request.metric:
            query_parts.append(analysis_request.metric)

        if analysis_request.dimensions:
            query_parts.append(
                "by " + ", ".join(analysis_request.dimensions)
            )

        if analysis_request.filters:
            query_parts.append(
                " ".join(analysis_request.filters)
            )

        if analysis_request.time_period:
            query_parts.append(analysis_request.time_period)

        if analysis_request.comparison:
            query_parts.append(
                "compared with " + analysis_request.comparison
            )

        query = " ".join(query_parts)

        return RAGRequest(
            query=query,
            top_k=5,
        )