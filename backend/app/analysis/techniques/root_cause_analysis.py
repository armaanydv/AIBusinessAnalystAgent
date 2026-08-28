from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.root_cause_data import RootCauseData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class RootCauseAnalysis(BaseAnalysis):
    """
    Performs root-cause analysis using retrieved business evidence.

    The LLM is responsible for extracting structured causes from
    the retrieved evidence and explaining their business impact.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ) -> AnalysisResult:
        """
        Perform root-cause analysis using the supplied
        analytical requirements and retrieved evidence.
        """

        evidence = self._build_evidence(retrieval_results)

        root_cause_data = self._extract_root_causes(
            request=request,
            evidence=evidence,
        )

        explanation = self._generate_explanation(
            request=request,
            root_cause_data=root_cause_data,
            evidence=evidence,
        )

        findings = [
            (
                f"{cause.cause}: {cause.impact}"
            )
            for cause in root_cause_data.causes
        ]

        return AnalysisResult(
            analysis_type="root_cause",
            findings=findings,
            conclusions=[explanation],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_root_causes(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> RootCauseData:
        """
        Use the LLM to extract structured root causes
        from the retrieved evidence.
        """

        prompt = f"""
You are a business data analysis assistant.

Identify the root causes relevant to the user's
business question using ONLY the retrieved evidence.

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
2. Do not invent causes, facts, values, or relationships.
3. Identify only causes that are explicitly supported by
   the retrieved evidence.
4. For every cause, provide the supporting evidence.
5. Describe the business impact only when supported by
   the evidence.
6. Return numerical values exactly when available.
7. Return ONLY valid JSON.
8. Do not include markdown or code fences.

Expected JSON:

{{
    "metric": "string",
    "current_period": "string",
    "previous_period": "string",
    "current_value": 0.0,
    "previous_value": 0.0,
    "causes": [
        {{
            "cause": "string",
            "evidence": "string",
            "impact": "string"
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
            RootCauseData,
        )

    def _generate_explanation(
        self,
        request: AnalysisRequest,
        root_cause_data: RootCauseData,
        evidence: str,
    ) -> str:
        """
        Ask the LLM to explain the identified root causes
        in business terms.
        """

        causes = "\n".join(
            (
                f"- Cause: {cause.cause}\n"
                f"  Evidence: {cause.evidence}\n"
                f"  Impact: {cause.impact}"
            )
            for cause in root_cause_data.causes
        )

        prompt = f"""
You are an expert AI Business Analyst.

Explain the root causes identified for the business question.

Business objective:
{request.objective}

Metric:
{root_cause_data.metric}

Previous period:
{root_cause_data.previous_period}

Previous value:
{root_cause_data.previous_value}

Current period:
{root_cause_data.current_period}

Current value:
{root_cause_data.current_value}

Identified causes:

{causes}

Retrieved evidence:

{evidence}

Rules:

1. Base the explanation ONLY on the supplied evidence.
2. Do not invent causes or relationships.
3. Clearly connect each identified cause to the observed
   business change when the evidence supports that connection.
4. Distinguish evidence from interpretation.
5. Do not claim causation when the evidence only indicates
   an association or management explanation.
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
        """
        Combine retrieved chunks into a single evidence block.
        """

        return "\n\n".join(
            result.chunk.text
            for result in retrieval_results
        )