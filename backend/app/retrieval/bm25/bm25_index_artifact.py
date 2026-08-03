from pydantic import BaseModel, ConfigDict, Field


class BM25IndexArtifact(BaseModel):
    """
    Serializable BM25 index artifact.
    """

    model_config = ConfigDict(extra="forbid")

    chunk_ids: list[str] = Field(
        default_factory=list,
    )

    tokenized_corpus: list[list[str]] = Field(
        default_factory=list,
    )