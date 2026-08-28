from app.analysis.analysis_request import AnalysisRequest
from app.analysis.analysis_result import AnalysisResult
from app.analysis.base_analysis import BaseAnalysis
from app.analysis.techniques.swot_data import SWOTData
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser
from app.retrieval.retriever.retrieval_result import RetrievalResult


class SWOTAnalysis(BaseAnalysis):
    """
    Performs SWOT analysis using retrieved business evidence.

    The LLM identifies strengths, weaknesses, opportunities,
    and threats from the supplied evidence.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(
        self,
        request: AnalysisRequest,
        retrieval_results: list[RetrievalResult],
    ) -> AnalysisResult:
        """
        Perform SWOT analysis using the supplied
        analytical requirements and retrieved evidence.
        """

        evidence = self._build_evidence(
            retrieval_results
        )

        swot_data = self._extract_swot_data(
            request=request,
            evidence=evidence,
        )

        conclusion = self._generate_conclusion(
            request=request,
            swot_data=swot_data,
            evidence=evidence,
        )

        findings = []

        if swot_data.strengths:
            findings.append(
                "Strengths: "
                + "; ".join(swot_data.strengths)
            )

        if swot_data.weaknesses:
            findings.append(
                "Weaknesses: "
                + "; ".join(swot_data.weaknesses)
            )

        if swot_data.opportunities:
            findings.append(
                "Opportunities: "
                + "; ".join(swot_data.opportunities)
            )

        if swot_data.threats:
            findings.append(
                "Threats: "
                + "; ".join(swot_data.threats)
            )

        return AnalysisResult(
            analysis_type="swot",
            findings=findings,
            conclusions=[conclusion],
            supporting_evidence=[
                result.chunk.text
                for result in retrieval_results
            ],
        )

    def _extract_swot_data(
        self,
        request: AnalysisRequest,
        evidence: str,
    ) -> SWOTData:
        """
        Use the LLM to extract SWOT factors
        from the retrieved evidence.
        """

        prompt = f"""
You are an expert business analyst.

Perform a SWOT analysis using ONLY the supplied
business evidence.

Business objective:
{request.objective}

Metric:
{request.metric}

Dimensions:
{request.dimensions}

Filters:
{request.filters}

Time period:
{request.time_period}

Retrieved evidence:

{evidence}

Identify:

1. Strengths
   Internal factors supported by the evidence that
   represent positive capabilities or performance.

2. Weaknesses
   Internal factors supported by the evidence that
   represent limitations, problems, or poor performance.

3. Opportunities
   External or future-oriented factors supported by the
   evidence that could create potential improvement or growth.

4. Threats
   External or future-oriented factors supported by the
   evidence that could negatively affect performance.

Rules:

1. Use ONLY information present in the retrieved evidence.
2. Do not invent facts.
3. Do not make unsupported assumptions.
4. Each item must be concise.
5. Return empty arrays when the evidence does not support
   a category.
6. Return ONLY valid JSON.
7. Do not include markdown or code fences.

Expected JSON:

{{
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "threats": []
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
            SWOTData,
        )

    def _generate_conclusion(
        self,
        request: AnalysisRequest,
        swot_data: SWOTData,
        evidence: str,
    ) -> str:
        """
        Generate a business-oriented interpretation of
        the SWOT findings.
        """

        prompt = f"""
You are an expert AI Business Analyst.

Provide a concise business interpretation of the
following SWOT analysis.

Business objective:
{request.objective}

Strengths:
{swot_data.strengths}

Weaknesses:
{swot_data.weaknesses}

Opportunities:
{swot_data.opportunities}

Threats:
{swot_data.threats}

Retrieved evidence:

{evidence}

Rules:

1. Base the explanation only on the supplied SWOT findings
   and retrieved evidence.
2. Do not invent causes, facts, or recommendations.
3. Clearly distinguish internal factors from external
   or future-oriented factors.
4. Explain the overall strategic position.
5. Keep the explanation concise.
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