from abc import ABC, abstractmethod

from app.analysis.analysis_request import AnalysisRequest
from app.retrieval.retriever.retrieval_result import RetrievalResult


class BaseAnalysis(ABC):
    """
    Abstract interface for all business analysis techniques.

    Each analysis technique receives the user's analytical
    requirements and the retrieved evidence, then produces
    an analysis result.
    """

    @abstractmethod
    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ):
        """
        Perform the analysis using the supplied requirements
        and retrieved evidence.
        """
        ...