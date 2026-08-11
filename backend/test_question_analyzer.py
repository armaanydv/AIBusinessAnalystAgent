from app.analysis.analysis_request import AnalysisRequest
from app.analysis.question_analyzer import QuestionAnalyzer
from app.llm.llm_response import LLMResponse


class FakeLLM:
    def generate(self, request):
        return LLMResponse(
            text="""{
                "metric": "revenue",
                "dimensions": ["region"],
                "filters": ["North"],
                "time_period": "last quarter",
                "comparison": "previous quarter",
                "objective": "explain decline",
                "analysis_type": "root cause analysis"
            }"""
        )


def test_question_analyzer_extracts_requirements():
    llm = FakeLLM()
    analyzer = QuestionAnalyzer(llm)

    request = analyzer.analyze(
        "Why did revenue decline in the North region last quarter?"
    )

    assert isinstance(request, AnalysisRequest)

    assert request.metric == "revenue"
    assert request.dimensions == ["region"]
    assert request.filters == ["North"]
    assert request.time_period == "last quarter"
    assert request.comparison == "previous quarter"
    assert request.objective == "explain decline"
    assert request.analysis_type == "root cause analysis"


def test_question_analyzer_detects_complete_request():
    llm = FakeLLM()
    analyzer = QuestionAnalyzer(llm)

    request = analyzer.analyze(
        "Why did revenue decline in the North region last quarter?"
    )

    assert request.is_complete() is True
    assert request.missing_requirements() == []