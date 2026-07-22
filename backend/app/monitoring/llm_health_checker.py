from dataclasses import dataclass
from time import perf_counter

from app.llm.base_llm import BaseLLM
from app.llm.llm_request import LLMRequest


@dataclass(slots=True, frozen=True)
class HealthCheckResult:
    healthy: bool
    latency_ms: float
    message: str


class LLMHealthChecker:
    """
    Performs operational health checks against an LLM provider.
    """

    def __init__(self, llm: BaseLLM):
        self._llm = llm

    def check(self) -> HealthCheckResult:
        """
        Returns the current health status of the configured LLM.
        """

        start = perf_counter()

        try:
            self._llm.generate(
                LLMRequest(
                    prompt="Reply with exactly: OK",
                    max_tokens=5,
                    temperature=0.0,
                )
            )

            latency = (perf_counter() - start) * 1000

            return HealthCheckResult(
                healthy=True,
                latency_ms=round(latency, 2),
                message="LLM is healthy.",
            )

        except Exception as exc:
            latency = (perf_counter() - start) * 1000

            return HealthCheckResult(
                healthy=False,
                latency_ms=round(latency, 2),
                message=str(exc),
            )