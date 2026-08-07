from dataclasses import dataclass

from app.core.settings import get_settings


@dataclass(slots=True, frozen=True)
class RerankerConfig:
    """
    Immutable runtime configuration for the CrossEncoder reranker.
    """

    model: str
    top_k: int
    batch_size: int


def get_reranker_config() -> RerankerConfig:
    settings = get_settings()

    return RerankerConfig(
        model=settings.reranker.model,
        top_k=settings.reranker.top_k,
        batch_size=settings.reranker.batch_size,
    )