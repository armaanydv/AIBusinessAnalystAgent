from pathlib import Path

from app.document.chunking.chunk_builder import ChunkBuilder
from app.document.hierarchy.hierarchy_builder import HierarchyBuilder
from app.document.indexing.index_builder import IndexBuilder
from app.document.relationships.relationship_builder import RelationshipBuilder

from app.ingestion.ingestion_service import IngestionService
from app.ingestion.parsers.docling_parser import DoclingParser

from app.preprocessing.document_preprocessor import DocumentPreprocessor

from app.providers.llm_provider import get_llm

from app.prompting.rag_prompt_builder import RAGPromptBuilder

from app.rag.rag_request import RAGRequest

from app.retrieval.embeddings.bge_embedding_model import BGEEmbeddingModel
from app.retrieval.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.retriever.semantic_retriever import SemanticRetriever
from app.retrieval.vector_store.faiss_vector_store import FAISSVectorStore

from app.services.rag_service import RAGService

from app.storage.artifact_storage import ArtifactStorage


def main():

    pdf_path = Path("sample.pdf")

    embedding_model = BGEEmbeddingModel()

    vector_store = FAISSVectorStore(
    dimension=embedding_model.dimension,
)

    ingestion_service = IngestionService(
        parser=DoclingParser(),
        preprocessor=DocumentPreprocessor(),
        index_builder=IndexBuilder(),
        relationship_builder=RelationshipBuilder(),
        hierarchy_builder=HierarchyBuilder(),
        chunk_builder=ChunkBuilder(),
        embedding_generator=EmbeddingGenerator(
            embedding_model=embedding_model,
        ),
        vector_store=vector_store,
        artifact_storage=ArtifactStorage(),
    )

    print("=" * 60)
    print("INGESTING DOCUMENT")
    print("=" * 60)

    document, chunks = ingestion_service.ingest(pdf_path)

    print(f"Document ID : {document.metadata.document_id}")
    print(f"Chunks      : {len(chunks.chunks)}")

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        chunks=chunks,
    )

    rag_service = RAGService(
        retriever=retriever,
        prompt_builder=RAGPromptBuilder(),
        llm=get_llm(),
    )

    while True:

        query = input("\nQuestion (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        request = RAGRequest(query=query)

        response = rag_service.generate(request)

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(response.answer)

        print("\nRetrieved Chunks:\n")

        for i, result in enumerate(response.retrieval_results, start=1):

            print(f"{i}. Score : {result.similarity_score:.4f}")
            print(result.chunk.text)
            print("-" * 60)


if __name__ == "__main__":
    main()
