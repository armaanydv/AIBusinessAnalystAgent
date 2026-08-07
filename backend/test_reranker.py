from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection
from app.document.chunking.chunk_metadata import ChunkMetadata

from app.retrieval.bm25.bm25_config import BM25Config
from app.retrieval.bm25.bm25_index import BM25Index
from app.retrieval.bm25.tokenizer import BM25Tokenizer

from app.retrieval.embeddings.bge_embedding_model import (
    BGEEmbeddingModel,
)
from app.retrieval.embeddings.embedding_generator import (
    EmbeddingGenerator,
)

from app.retrieval.fusion.reciprocal_rank_fusion import (
    ReciprocalRankFusion,
)

from app.retrieval.repository.chunk_repository import (
    ChunkRepository,
)

from app.retrieval.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.retrieval.retriever.bm25_retriever import (
    BM25Retriever,
)
from app.retrieval.retriever.hybrid_retriever import (
    HybridRetriever,
)
from app.retrieval.retriever.semantic_retriever import (
    SemanticRetriever,
)

from app.retrieval.vector_store.faiss_vector_store import (
    FAISSVectorStore,
)
from app.retrieval.vector_store.vector_record import (
    VectorRecord,
)

# ==========================================================
# Sample Chunks
# ==========================================================

chunks = ChunkCollection(
    chunks=[
        Chunk(
            id="chunk_1",
            title="Artificial Intelligence",
            text=(
                "Artificial Intelligence improves hospitals by "
                "helping doctors diagnose diseases faster and "
                "more accurately."
            ),
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=1,
                end_page=1,
                hierarchy_level=1,
            ),
        ),
        Chunk(
            id="chunk_2",
            title="Machine Learning",
            text=(
                "Machine learning algorithms require high-quality "
                "training data to achieve good performance."
            ),
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=2,
                end_page=2,
                hierarchy_level=1,
            ),
        ),
        Chunk(
            id="chunk_3",
            title="Finance",
            text=(
                "Financial reports summarize revenue, expenses, "
                "profit and business performance."
            ),
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=3,
                end_page=3,
                hierarchy_level=1,
            ),
        ),
    ]
)

# ==========================================================
# Repository
# ==========================================================

chunk_repository = ChunkRepository()

chunk_repository.add_many(
    chunks,
)

# ==========================================================
# Embeddings
# ==========================================================

embedding_model = BGEEmbeddingModel()

embedding_generator = EmbeddingGenerator(
    embedding_model=embedding_model,
)

embeddings = embedding_generator.generate(
    chunks,
)

# ==========================================================
# Vector Store
# ==========================================================

vector_store = FAISSVectorStore(
    dimension=embedding_model.dimension,
)

records = [
    VectorRecord(
        chunk_id=embedding.chunk_id,
        vector=embedding.vector,
    )
    for embedding in embeddings
]

vector_store.add_many(
    records,
)

# ==========================================================
# BM25
# ==========================================================

bm25_index = BM25Index(
    tokenizer=BM25Tokenizer(),
    config=BM25Config(),
)

bm25_index.build(
    chunks,
)

# ==========================================================
# Retrievers
# ==========================================================

semantic_retriever = SemanticRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
    chunk_repository=chunk_repository,
)

bm25_retriever = BM25Retriever(
    index=bm25_index,
    chunk_repository=chunk_repository,
)

fusion = ReciprocalRankFusion()

hybrid_retriever = HybridRetriever(
    semantic_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
    fusion=fusion,
)

# ==========================================================
# Reranker
# ==========================================================

reranker = CrossEncoderReranker()

# ==========================================================
# Query
# ==========================================================

query = "How does AI help hospitals?"

retrieval_results = hybrid_retriever.retrieve(
    query=query,
    k=3,
)

print()
print("=" * 80)
print("HYBRID RETRIEVAL")
print("=" * 80)

for result in retrieval_results:

    print(f"Rank            : {result.rank}")
    print(f"Chunk ID        : {result.chunk.id}")
    print(f"Hybrid Score    : {result.similarity_score:.6f}")
    print(f"Title           : {result.chunk.title}")
    print(f"Text            : {result.chunk.text}")
    print("-" * 80)

reranked_results = reranker.rerank(
    query=query,
    retrieval_results=retrieval_results,
    k=3,
)

print()
print("=" * 80)
print("CROSS ENCODER RERANKING")
print("=" * 80)

for result in reranked_results:

    print(f"Rank            : {result.rank}")
    print(f"Chunk ID        : {result.chunk.id}")
    print(f"Hybrid Score    : {result.retrieval_score:.6f}")
    print(f"Rerank Score    : {result.rerank_score:.6f}")
    print(f"Title           : {result.chunk.title}")
    print(f"Text            : {result.chunk.text}")
    print("-" * 80)