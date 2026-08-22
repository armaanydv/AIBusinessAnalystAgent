from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class AnalysisResult:
    """
    Represents the result produced by a business analysis
    technique.
    """

    analysis_type: str

    findings: list[str] = field(default_factory=list)

    conclusions: list[str] = field(default_factory=list)

    supporting_evidence: list[str] = field(
        default_factory=list
    )