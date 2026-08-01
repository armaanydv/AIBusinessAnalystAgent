from app.document.chunking.chunk import Chunk
from app.document.chunking.chunk_collection import ChunkCollection
from app.document.chunking.chunk_metadata import ChunkMetadata
from app.retrieval.bm25.bm25_config import BM25Config
from app.retrieval.bm25.bm25_index import BM25Index
from app.retrieval.bm25.tokenizer import BM25Tokenizer
from app.retrieval.retriever.bm25_retriever import BM25Retriever


chunks = ChunkCollection(
    chunks=[
        Chunk(
            id="chunk_1",
            text="Artificial Intelligence is transforming healthcare.",
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=1,
                end_page=1,
                hierarchy_level=1,
            ),
        ),
        Chunk(
            id="chunk_2",
            text="Machine learning models require quality data.",
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=2,
                end_page=2,
                hierarchy_level=1,
            ),
        ),
        Chunk(
            id="chunk_3",
            text="Financial reports summarize business performance.",
            metadata=ChunkMetadata(
                source_document="test.pdf",
                start_page=3,
                end_page=3,
                hierarchy_level=1,
            ),
        ),
    ]
)

tokenizer = BM25Tokenizer()

config = BM25Config()

index = BM25Index(
    tokenizer=tokenizer,
    config=config,
)

retriever = BM25Retriever(
    bm25_index=index,
)

retriever.set_chunks(chunks)

results = retriever.retrieve(
    query="artificial intelligence",
    k=3,
)

print("\nBM25 Results")
print("=" * 60)

for result in results:
    print(f"Rank     : {result.rank}")
    print(f"Chunk ID : {result.chunk.id}")
    print(f"Score    : {result.similarity_score:.4f}")
    print(f"Text     : {result.chunk.text}")
    print("-" * 60)