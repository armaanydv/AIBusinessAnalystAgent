from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BM25Config:
    """
    Configuration for the BM25 retrieval engine.
    """

    k1: float = 1.5

    b: float = 0.75