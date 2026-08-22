from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.analysis_selector import AnalysisSelector
from app.analysis.question_analyzer import QuestionAnalyzer
from app.analysis.retrieval_planner import RetrievalPlanner
from app.services.rag_service import RAGService


class AnalysisService:
    """
    Orchestrates the complete business analysis pipeline.

    Flow:
        User query
            ↓
        QuestionAnalyzer
            ↓
        AnalysisRequest
            ↓
        RetrievalPlanner
            ↓
        RAGService
            ↓
        Retrieved evidence
            ↓
        AnalysisSelector
            ↓
        Analysis technique
            ↓
        AnalysisResult
    """

    def __init__(
        self,
        question_analyzer: QuestionAnalyzer,
        retrieval_planner: RetrievalPlanner,
        rag_service: RAGService,
        analysis_selector: AnalysisSelector,
    ) -> None:
        self._question_analyzer = question_analyzer
        self._retrieval_planner = retrieval_planner
        self._rag_service = rag_service
        self._analysis_selector = analysis_selector

    def analyze(
        self,
        query: str,
    ) -> AnalysisResult:
        """
        Analyze a user's business question.
        """

        # --------------------------------------------------
        # 1. Understand the question
        # --------------------------------------------------

        analysis_request = self._question_analyzer.analyze(
            query
        )

        # --------------------------------------------------
        # 2. Make sure the question contains the requirements
        #    needed to perform an analysis.
        # --------------------------------------------------

        if not analysis_request.is_complete():
            missing = analysis_request.missing_requirements()

            raise ValueError(
                "Missing analysis requirements: "
                + ", ".join(missing)
            )

        # --------------------------------------------------
        # 3. Construct retrieval request from the
        #    available analytical requirements.
        # --------------------------------------------------

        retrieval_request = self._retrieval_planner.plan(
            analysis_request
        )

        # --------------------------------------------------
        # 4. Retrieve and rerank relevant evidence.
        # --------------------------------------------------

        retrieval_results = self._rag_service.retrieve(
            retrieval_request
        )

        # --------------------------------------------------
        # 5. Select the required analysis technique.
        # --------------------------------------------------

        analysis = self._analysis_selector.select(
            analysis_request.analysis_type
        )

        # --------------------------------------------------
        # 6. Perform the actual business analysis.
        # --------------------------------------------------

        return analysis.analyze(
            request=analysis_request,
            retrieval_results=retrieval_results,
        )