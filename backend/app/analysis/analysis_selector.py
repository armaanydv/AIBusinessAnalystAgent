from app.analysis.base_analysis import BaseAnalysis


class AnalysisSelector:
    """
    Selects the appropriate business analysis technique
    based on the requested analysis type.
    """

    def __init__(
        self,
        analyses: dict[str, BaseAnalysis],
    ) -> None:
        self._analyses = analyses

    def select(
        self,
        analysis_type: str,
    ) -> BaseAnalysis:
        """
        Return the analysis technique corresponding
        to the requested analysis type.
        """

        key = analysis_type.strip().lower()

        if key not in self._analyses:
            raise ValueError(
                f"Unsupported analysis type: {analysis_type}"
            )

        return self._analyses[key]