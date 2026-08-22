from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.comparison_data import ComparisonData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class ComparativeAnalysis(BaseAnalysis):
    """
    Performs comparative business analysis using retrieved evidence.

    The LLM is used to extract structured comparison data and
    explain the calculated results. Numerical calculations are
    performed deterministically in Python.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ) -> AnalysisResult:
        """
        Perform comparative analysis using the supplied
        analytical requirements and retrieved evidence.
        """

        evidence = self._build_evidence(retrieval_results)

        comparison_data = self._extract_comparison_data(
            request=request,
            evidence=evidence,
        )

        absolute_change = (
            comparison_data.current_value
            - comparison_data.previous_value
        )

        percentage_change = self._calculate_percentage_change(
            current_value=comparison_data.current_value,
            previous_value=comparison_data.previous_value,
        )

        explanation = self._generate_explanation(
            request=request,
            comparison_data=comparison_data,
            absolute_change=absolute_change,
            percentage_change=percentage_change,
            evidence=evidence,
        )

        return AnalysisResult(
            analysis_type="comparative",
            findings=[
                (
                    f"{comparison_data.metric} changed by "
                    f"{absolute_change} "
                    f"({percentage_change:.2f}%) "
                    f"from {comparison_data.previous_period} "
                    f"to {comparison_data.current_period}."
                )
            ],
            conclusions=[explanation],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_comparison_data(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> ComparisonData:
        """
        Use the LLM to extract structured numerical data
        from the retrieved evidence.
        """

        prompt = f"""
You are a business data extraction assistant.

Extract the numerical comparison required to answer the
business question.

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
3. current_value must represent the value for the requested
   time period.
4. previous_value must represent the value for the comparison
   period.
5. Return ONLY valid JSON.
6. If a dimension is not present, return null.
7. Values must be numerical.

Expected JSON:

{{
    "metric": "string",
    "current_value": 0.0,
    "previous_value": 0.0,
    "current_period": "string",
    "previous_period": "string",
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
            ComparisonData,
        )

    def _generate_explanation(
        self,
        request: AnalysisRequest,
        comparison_data: ComparisonData,
        absolute_change: float,
        percentage_change: float,
        evidence: str,
    ) -> str:
        """
        Ask the LLM to explain the calculated comparison
        in business terms.
        """

        prompt = f"""
You are an expert AI Business Analyst.

Explain the result of the following business comparison.

Business objective:
{request.objective}

Metric:
{comparison_data.metric}

Dimension:
{comparison_data.dimension}

Dimension value:
{comparison_data.dimension_value}

Current period:
{comparison_data.current_period}

Current value:
{comparison_data.current_value}

Previous period:
{comparison_data.previous_period}

Previous value:
{comparison_data.previous_value}

Absolute change:
{absolute_change}

Percentage change:
{percentage_change:.2f}%

Retrieved evidence:

{evidence}

Explain the result clearly and concisely.

Rules:

1. Do not invent causes or facts.
2. Base the explanation only on the supplied evidence
   and calculated values.
3. Clearly state whether the metric increased or decreased.
4. Mention the magnitude of the change.
5. Return only the explanation text.
"""

        response = self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        return response.text.strip()

    @staticmethod
    def _calculate_percentage_change(
        current_value: float,
        previous_value: float,
    ) -> float:
        """
        Calculate percentage change between two values.
        """

        if previous_value == 0:
            return 0.0

        return (
            (current_value - previous_value)
            / previous_value
        ) * 100

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