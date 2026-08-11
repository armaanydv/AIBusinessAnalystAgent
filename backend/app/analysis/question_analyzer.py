from app.analysis.analysis_request import AnalysisRequest
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser


class QuestionAnalyzer:
    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(self, query: str) -> AnalysisRequest:
        prompt = self._build_prompt(query)

        request = LLMRequest(
            prompt=prompt,
            response_format=ResponseFormat.JSON,
        )

        response = self._llm.generate(request)

        return OutputParser.parse(
            response,
            AnalysisRequest,
        )

    def _build_prompt(self, query: str) -> str:
        return f"""
You are an expert AI Business Analyst.

Analyze the following business question and extract its
analytical requirements.

Extract the following:

- metric
- dimensions
- filters
- time_period
- comparison
- objective
- analysis_type

Rules:
1. Do not invent information.
2. If a requirement cannot be determined, return null.
3. Return dimensions and filters as arrays of strings.
4. Return ONLY valid JSON.
5. Do not include markdown or code fences.

Expected JSON structure:

{{
    "metric": "string or null",
    "dimensions": [],
    "filters": [],
    "time_period": "string or null",
    "comparison": "string or null",
    "objective": "string or null",
    "analysis_type": "string or null"
}}

Business question:
{query}
"""