from sentence_transformers import SentenceTransformer

from app.retrieval.embeddings.base_embedding_model import BaseEmbeddingModel


class BGEEmbeddingModel(BaseEmbeddingModel):
    """
    BAAI BGE embedding model implementation.
    """

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    VECTOR_DIMENSION = 384

    def __init__(self):

        self.model = SentenceTransformer(
            self.MODEL_NAME
        )

    @property
    def model_name(self) -> str:

        return self.MODEL_NAME

    @property
    def dimension(self) -> int:

        return self.VECTOR_DIMENSION

    def encode(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate normalized embeddings.
        """

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return vectors.tolist()