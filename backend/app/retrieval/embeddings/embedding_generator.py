from app.document.chunking.chunk_collection import ChunkCollection
from app.retrieval.embeddings.base_embedding_model import BaseEmbeddingModel
from app.retrieval.embeddings.embedding import Embedding


class EmbeddingGenerator:
    """
    Generates embeddings for semantic document chunks.
    """

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
    ):

        self.embedding_model = embedding_model

    def generate(
        self,
        chunks: ChunkCollection,
    ) -> list[Embedding]:
        """
        Generate embeddings for every chunk.
        """

        if not chunks.chunks:
            return []

        # ----------------------------------------------------------
        # Collect chunk texts
        # ----------------------------------------------------------

        texts = [
            chunk.text
            for chunk in chunks.chunks
        ]

        # ----------------------------------------------------------
        # Batch embedding
        # ----------------------------------------------------------

        vectors = self.embedding_model.encode(
            texts
        )

        # ----------------------------------------------------------
        # Build Embedding objects
        # ----------------------------------------------------------

        embeddings = []

        for chunk, vector in zip(
            chunks.chunks,
            vectors,
        ):

            embeddings.append(
                Embedding(
                    chunk_id=chunk.id,
                    vector=vector,
                    model_name=self.embedding_model.model_name,
                    dimension=self.embedding_model.dimension,
                )
            )

        return embeddings