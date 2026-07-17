from docling.document_converter import DocumentConverter

from app.ingestion.mappers.docling_mapper import DoclingMapper
from app.retrieval.embeddings.bge_embedding_model import BGEEmbeddingModel
from app.retrieval.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.retriever.semantic_retriever import SemanticRetriever
from app.retrieval.vector_store.faiss_vector_store import FAISSVectorStore
from app.retrieval.vector_store.vector_record import VectorRecord


# ==========================================================
# Parse PDF
# ==========================================================

converter = DocumentConverter()

result = converter.convert("sample.pdf")

docling_document = result.document


# ==========================================================
# Map Document
# ==========================================================

mapper = DoclingMapper()

structured_document = mapper.map(docling_document)


# ==========================================================
# Generate Embeddings
# ==========================================================

embedding_model = BGEEmbeddingModel()

embedding_generator = EmbeddingGenerator(
    embedding_model
)

embeddings = embedding_generator.generate(
    structured_document.chunks
)

print(f"\nGenerated {len(embeddings)} embeddings.")


# ==========================================================
# Build Vector Store
# ==========================================================

vector_store = FAISSVectorStore(
    dimension=embedding_model.dimension
)

records = [
    VectorRecord(
        chunk_id=embedding.chunk_id,
        vector=embedding.vector,
    )
    for embedding in embeddings
]

vector_store.add_many(records)

print(
    f"Indexed {vector_store.size} vectors."
)


# ==========================================================
# Semantic Retriever
# ==========================================================

retriever = SemanticRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
    chunks=structured_document.chunks,
)


# ==========================================================
# Query
# ==========================================================

query = input(
    "\nAsk a question: "
)

results = retriever.retrieve(
    query=query,
    k=5,
)


# ==========================================================
# Results
# ==========================================================

print("\n")
print("=" * 100)
print("SEARCH RESULTS")
print("=" * 100)

for rank, result in enumerate(results, start=1):

    print(f"\nResult {rank}")
    print("-" * 100)

    print(
        f"Score : {result.similarity_score:.4f}"
    )

    print(
        f"Title : {result.chunk.title}"
    )

    print(
        f"Pages : "
        f"{result.chunk.metadata.start_page}"
        f"-"
        f"{result.chunk.metadata.end_page}"
    )

    print("\nText\n")

    print(result.chunk.text)

    print()