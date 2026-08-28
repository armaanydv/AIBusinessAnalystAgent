from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.trend_data import TrendData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class TrendAnalysis(BaseAnalysis):
    """
    Performs trend analysis using retrieved business evidence.

    The LLM extracts structured time-series data and explains
    the calculated trend. Numerical calculations are performed
    deterministically in Python.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ) -> AnalysisResult:

        evidence = self._build_evidence(retrieval_results)

        trend_data = self._extract_trend_data(
            request=request,
            evidence=evidence,
        )

        self._validate_trend_data(trend_data)

        period_changes = self._calculate_period_changes(
            trend_data.values
        )

        overall_change = (
            trend_data.values[-1]
            - trend_data.values[0]
        )

        overall_percentage_change = (
            self._calculate_percentage_change(
                current_value=trend_data.values[-1],
                previous_value=trend_data.values[0],
            )
        )

        direction = self._determine_direction(
            trend_data.values
        )

        explanation = self._generate_explanation(
            request=request,
            trend_data=trend_data,
            direction=direction,
            period_changes=period_changes,
            overall_change=overall_change,
            overall_percentage_change=overall_percentage_change,
            evidence=evidence,
        )

        return AnalysisResult(
            analysis_type="trend",
            findings=[
                (
                    f"{trend_data.metric} shows a "
                    f"{direction} trend from "
                    f"{trend_data.periods[0]} to "
                    f"{trend_data.periods[-1]}, "
                    f"changing by "
                    f"{overall_change:.2f} "
                    f"({overall_percentage_change:.2f}%)."
                )
            ],
            conclusions=[explanation],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_trend_data(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> TrendData:
        """
        Use the LLM to extract ordered time-series data
        from retrieved evidence.
        """

        prompt = f"""
You are a business data extraction assistant.

Extract the time-series data required to answer the
business trend question.

Analytical requirements:

Metric:
{request.metric}

Dimensions:
{request.dimensions}

Filters:
{request.filters}

Time period:
{request.time_period}

Comparison:
{request.comparison}

Objective:
{request.objective}

Retrieved evidence:

{evidence}

Rules:

1. Use ONLY information present in the retrieved evidence.
2. Do not invent values.
3. Extract all relevant periods required to analyze the trend.
4. periods and values must have the same length.
5. periods must be ordered chronologically.
6. Values must be numerical.
7. If a dimension is not present, return null.
8. Return ONLY valid JSON.

Expected JSON:

{{
    "metric": "string",
    "periods": ["string"],
    "values": [0.0],
    "dimension": "string or null",
    "dimension_value": "string or null"
}}
"""

        response = self._llm.generate(
            LLMRequest(
                prompt=prompt,
                response_format=ResponseFormat.JSON,
            )
        )

        return OutputParser.parse(
            response,
            TrendData,
        )

    def _generate_explanation(
        self,
        request: AnalysisRequest,
        trend_data: TrendData,
        direction: str,
        period_changes: list[float],
        overall_change: float,
        overall_percentage_change: float,
        evidence: str,
    ) -> str:
        """
        Ask the LLM to explain the calculated trend
        in business terms.
        """

        changes_text = "\n".join(
            (
                f"{trend_data.periods[index]} → "
                f"{trend_data.periods[index + 1]}: "
                f"{change:.2f}%"
            )
            for index, change in enumerate(period_changes)
        )

        prompt = f"""
You are an expert AI Business Analyst.

Explain the following business trend.

Business objective:
{request.objective}

Metric:
{trend_data.metric}

Dimension:
{trend_data.dimension}

Dimension value:
{trend_data.dimension_value}

Periods:
{trend_data.periods}

Values:
{trend_data.values}

Trend direction:
{direction}

Period-over-period changes:
{changes_text}

Overall absolute change:
{overall_change}

Overall percentage change:
{overall_percentage_change:.2f}%

Retrieved evidence:

{evidence}

Rules:

1. Do not invent causes or facts.
2. Base the explanation only on the supplied evidence
   and calculated values.
3. Clearly describe the direction of the trend.
4. Mention the overall magnitude of change.
5. Mention notable acceleration or deceleration only when
   supported by the calculated values.
6. Return only the explanation text.
"""

        response = self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        return response.text.strip()

    @staticmethod
    def _calculate_period_changes(
        values: list[float],
    ) -> list[float]:
        """
        Calculate percentage change between each
        consecutive period.
        """

        changes = []

        for index in range(1, len(values)):
            previous_value = values[index - 1]
            current_value = values[index]

            changes.append(
                TrendAnalysis._calculate_percentage_change(
                    current_value=current_value,
                    previous_value=previous_value,
                )
            )

        return changes

    @staticmethod
    def _calculate_percentage_change(
        current_value: float,
        previous_value: float,
    ) -> float:
        """
        Calculate percentage change.
        """

        if previous_value == 0:
            return 0.0

        return (
            (current_value - previous_value)
            / previous_value
        ) * 100

    @staticmethod
    def _determine_direction(
        values: list[float],
    ) -> str:
        """
        Determine the overall direction of the trend.
        """

        if values[-1] > values[0]:
            return "increasing"

        if values[-1] < values[0]:
            return "decreasing"

        return "stable"

    @staticmethod
    def _validate_trend_data(
        trend_data: TrendData,
    ) -> None:
        """
        Validate that sufficient time-series data exists.
        """

        if len(trend_data.periods) < 2:
            raise ValueError(
                "Trend analysis requires at least two periods."
            )

        if len(trend_data.periods) != len(
            trend_data.values
        ):
            raise ValueError(
                "Trend periods and values must have "
                "the same length."
            )

    @staticmethod
    def _build_evidence(
        retrieval_results: list[RetrievalResult],
    ) -> str:
        """
        Combine retrieved chunks into a single evidence block.
        """

        return "\n\n".join(
            result.chunk.text
            for result in retrieval_results
        )