from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.contribution_data import ContributionData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class ContributionAnalysis(BaseAnalysis):
    """
    Performs contribution analysis using retrieved business evidence.

    The LLM extracts the individual contributors and their changes.
    Contribution percentages are calculated deterministically in Python.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ) -> AnalysisResult:

        evidence = self._build_evidence(retrieval_results)

        contribution_data = self._extract_contributions(
            request=request,
            evidence=evidence,
        )

        contributions = self._calculate_contributions(
            contribution_data
        )

        explanation = self._generate_explanation(
            request=request,
            contribution_data=contribution_data,
            contributions=contributions,
            evidence=evidence,
        )

        findings = [
            (
                f"{item['contributor']} contributed "
                f"{item['change']:.2f} "
                f"to the total change "
                f"({item['contribution_percentage']:.2f}%)."
            )
            for item in contributions
        ]

        return AnalysisResult(
            analysis_type="contribution",
            findings=findings,
            conclusions=[explanation],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_contributions(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> ContributionData:

        prompt = f"""
You are a business data extraction assistant.

Identify the individual contributors to the change described
in the business question.

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
2. Do not invent contributors or values.
3. Identify the individual components that contributed
   to the requested change.
4. Extract the actual numerical change for each contributor.
5. Return the total change when it is explicitly available.
6. Return ONLY valid JSON.
7. Do not include markdown or code fences.
8. contribution_percentage may be returned as 0.0 because
   it will be calculated deterministically.

Expected JSON:

{{
    "metric": "string",
    "current_period": "string",
    "previous_period": "string",
    "total_change": 0.0,
    "contributions": [
        {{
            "contributor": "string",
            "change": 0.0,
            "contribution_percentage": 0.0
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
            ContributionData,
        )

    @staticmethod
    def _calculate_contributions(
        data: ContributionData,
    ) -> list[dict]:

        if data.total_change == 0:
            return [
                {
                    "contributor": item.contributor,
                    "change": item.change,
                    "contribution_percentage": 0.0,
                }
                for item in data.contributions
            ]

        return [
            {
                "contributor": item.contributor,
                "change": item.change,
                "contribution_percentage": (
                    item.change / data.total_change
                ) * 100,
            }
            for item in data.contributions
        ]

    def _generate_explanation(
        self,
        request: AnalysisRequest,
        contribution_data: ContributionData,
        contributions: list[dict],
        evidence: str,
    ) -> str:

        contribution_text = "\n".join(
            (
                f"- {item['contributor']}: "
                f"{item['change']:.2f} "
                f"({item['contribution_percentage']:.2f}%)"
            )
            for item in contributions
        )

        prompt = f"""
You are an expert AI Business Analyst.

Explain which contributors had the greatest impact on the
business change described below.

Business objective:
{request.objective}

Metric:
{contribution_data.metric}

Previous period:
{contribution_data.previous_period}

Current period:
{contribution_data.current_period}

Total change:
{contribution_data.total_change}

Calculated contributions:

{contribution_text}

Retrieved evidence:

{evidence}

Rules:

1. Base the explanation ONLY on the supplied evidence
   and calculated contribution values.
2. Do not invent causes or facts.
3. Identify the largest contributors.
4. Explain each contributor's relative contribution.
5. Clearly distinguish contribution from causation.
6. Do not claim that a contributor caused the change unless
   the evidence explicitly supports that conclusion.
7. Return only the explanation text.
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