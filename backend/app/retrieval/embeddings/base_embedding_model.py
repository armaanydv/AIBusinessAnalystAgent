from abc import ABC, abstractmethod


class BaseEmbeddingModel(ABC):
    """
    Abstract base class for all embedding models.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Name of the embedding model.
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Dimension of the embedding vectors.
        """
        pass

    @abstractmethod
    def encode(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a batch of texts.
        """
        pass