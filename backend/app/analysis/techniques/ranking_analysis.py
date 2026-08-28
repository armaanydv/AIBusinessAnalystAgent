from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.ranking_data import RankingData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class RankingAnalysis(BaseAnalysis):
    """
    Performs ranking analysis using retrieved business evidence.

    The LLM extracts the required numerical data.
    Ranking and numerical calculations are performed
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

        ranking_data = self._extract_ranking_data(
            request=request,
            evidence=evidence,
        )

        ranked_items = self._calculate_ranking(
            ranking_data
        )

        winner = ranked_items[0]

        explanation = self._generate_explanation(
            request=request,
            ranking_data=ranking_data,
            ranked_items=ranked_items,
            evidence=evidence,
        )

        return AnalysisResult(
            analysis_type="ranking",
            findings=[
                (
                    f"{winner['dimension_value']} had the largest "
                    f"{ranking_data.metric} growth from "
                    f"{ranking_data.previous_period} to "
                    f"{ranking_data.current_period}, "
                    f"increasing by {winner['absolute_change']:.2f} "
                    f"({winner['percentage_change']:.2f}%)."
                )
            ],
            conclusions=[explanation],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_ranking_data(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> RankingData:

        prompt = f"""
You are a business data extraction assistant.

Extract all numerical data required to answer the
business ranking question.

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
3. Extract every relevant dimension value.
4. current_value must correspond to the requested current period.
5. previous_value must correspond to the comparison period.
6. Return ONLY valid JSON.
7. Values must be numerical.

Expected JSON:

{{
    "metric": "string",
    "current_period": "string",
    "previous_period": "string",
    "items": [
        {{
            "dimension_value": "string",
            "current_value": 0.0,
            "previous_value": 0.0
        }}
    ]
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
            RankingData,
        )

    @staticmethod
    def _calculate_ranking(
        ranking_data: RankingData,
    ) -> list[dict]:

        ranked_items = []

        for item in ranking_data.items:

            absolute_change = (
                item.current_value
                - item.previous_value
            )

            if item.previous_value == 0:
                percentage_change = 0.0
            else:
                percentage_change = (
                    absolute_change
                    / item.previous_value
                ) * 100

            ranked_items.append(
                {
                    "dimension_value": item.dimension_value,
                    "current_value": item.current_value,
                    "previous_value": item.previous_value,
                    "absolute_change": absolute_change,
                    "percentage_change": percentage_change,
                }
            )

        ranked_items.sort(
            key=lambda item: item["absolute_change"],
            reverse=True,
        )

        return ranked_items

    def _generate_explanation(
        self,
        request: AnalysisRequest,
        ranking_data: RankingData,
        ranked_items: list[dict],
        evidence: str,
    ) -> str:

        ranking_summary = "\n".join(
            (
                f"{index}. {item['dimension_value']}: "
                f"{item['previous_value']} → "
                f"{item['current_value']} "
                f"(change: {item['absolute_change']:.2f}, "
                f"{item['percentage_change']:.2f}%)"
            )
            for index, item in enumerate(
                ranked_items,
                start=1,
            )
        )

        prompt = f"""
You are an expert AI Business Analyst.

Explain the ranking result for the following business question.

Business objective:
{request.objective}

Metric:
{ranking_data.metric}

Previous period:
{ranking_data.previous_period}

Current period:
{ranking_data.current_period}

Calculated ranking:

{ranking_summary}

Retrieved evidence:

{evidence}

Rules:

1. Do not invent causes or facts.
2. Use only the supplied evidence and calculated values.
3. Clearly identify the highest-ranked dimension.
4. Mention its absolute and percentage change.
5. Briefly compare it with the other dimensions when useful.
6. Return only the explanation text.
"""

        response = self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        return response.text.strip()

    @staticmethod
    def _build_evidence(
        retrieval_results: list[RetrievalResult],
    ) -> str:

        return "\n\n".join(
            result.chunk.text
            for result in retrieval_results
        )