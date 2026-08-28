from app.analysis.analysis_request import AnalysisRequest
from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest, ResponseFormat
from app.llm.output_parser import OutputParser


class QuestionAnalyzer:
    """
    Analyzes a user's business question and extracts the
    analytical requirements needed by the analysis pipeline.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    def analyze(self, query: str) -> AnalysisRequest:
        """
        Analyze a business question and return its
        structured analytical requirements.
        """

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

6. analysis_type MUST be one of the following values:
   - comparative
   - trend
   - ranking
   - root_cause
   - contribution
   - swot

7. Use "ranking" when the question asks to:
   - identify the highest or lowest performing dimension
   - find which region, product, category, or segment performed best or worst
   - determine the largest or smallest growth
   - rank multiple dimensions by a metric
   - identify the top or bottom performer

8. Use "comparative" when the question asks to compare
   specific values between two periods, dimensions, or groups
   without asking for the highest, lowest, best, worst, or ranking.

9. Use "trend" when the question asks about the direction,
   pattern, or trajectory of a metric across multiple periods.

10. Use "root_cause" when the question asks why a metric,
    event, increase, decrease, or change occurred.

11. Use "contribution" when the question asks which factors,
    dimensions, categories, or components contributed to a
    total change or outcome.

12. Use "swot" when the question explicitly asks for a
    strengths, weaknesses, opportunities, and threats analysis.

13. If the question does not clearly correspond to one of
    the supported analysis types, return null for analysis_type.

14. Use the exact analysis_type values listed above.

15. Do not combine multiple analysis types into one value.

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