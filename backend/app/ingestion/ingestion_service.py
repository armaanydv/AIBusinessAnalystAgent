from app.document.chunking.chunk_builder import ChunkBuilder
from app.document.chunking.chunk_collection import ChunkCollection
from app.document.hierarchy.hierarchy_builder import HierarchyBuilder
from app.document.indexing.index_builder import IndexBuilder
from app.document.relationships.relationship_builder import RelationshipBuilder

from app.ingestion.parsers.base_parser import BaseParser

from app.models.structured_document import StructuredDocument

from app.preprocessing.document_preprocessor import DocumentPreprocessor

from app.retrieval.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store.base_vector_store import BaseVectorStore
from app.retrieval.vector_store.vector_record import VectorRecord

from app.storage.artifact_storage import ArtifactStorage


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.
    """

    def __init__(
        self,
        parser: BaseParser,
        preprocessor: DocumentPreprocessor,
        index_builder: IndexBuilder,
        relationship_builder: RelationshipBuilder,
        hierarchy_builder: HierarchyBuilder,
        chunk_builder: ChunkBuilder,
        embedding_generator: EmbeddingGenerator,
        vector_store: BaseVectorStore,
        artifact_storage: ArtifactStorage,
    ) -> None:

        self._parser = parser
        self._preprocessor = preprocessor
        self._index_builder = index_builder
        self._relationship_builder = relationship_builder
        self._hierarchy_builder = hierarchy_builder
        self._chunk_builder = chunk_builder
        self._embedding_generator = embedding_generator
        self._vector_store = vector_store
        self._artifact_storage = artifact_storage

    def ingest(
        self,
        file_path: str,
    ) -> tuple[StructuredDocument, ChunkCollection]:

        # ---------------------------------------------------------
        # Parse
        # ---------------------------------------------------------

        parsed_document = self._parser.parse(file_path)

        document = parsed_document.structured_document

        # ---------------------------------------------------------
        # Preprocess
        # ---------------------------------------------------------

        document = self._preprocessor.preprocess(document)

        # ---------------------------------------------------------
        # Build document artifacts
        # ---------------------------------------------------------

        document.index = self._index_builder.build(document)

        document.relationship_graph = self._relationship_builder.build(
            parsed_document.docling_document,
            document,
        )

        document.hierarchy_tree = self._hierarchy_builder.build(document)

        chunks = self._chunk_builder.build(document)

        # ---------------------------------------------------------
        # Generate embeddings
        # ---------------------------------------------------------

        embeddings = self._embedding_generator.generate(chunks)

        # ---------------------------------------------------------
        # Convert Embeddings -> VectorRecords
        # ---------------------------------------------------------

        records = [
            VectorRecord(
                chunk_id=embedding.chunk_id,
                vector=embedding.vector,
            )
            for embedding in embeddings
        ]

        # ---------------------------------------------------------
        # Index vectors
        # ---------------------------------------------------------

        self._vector_store.add_many(records)

        # ---------------------------------------------------------
        # Persist artifacts
        # ---------------------------------------------------------

        document_id = document.metadata.document_id

        # self._artifact_storage.save_document(
        #     document_id=document_id,
        #     document=document,
        # )

        # self._artifact_storage.save_chunks(
        #     document_id=document_id,
        #     chunks=chunks,
        # )

        # self._artifact_storage.save_vector_store(
        #     document_id=document_id,
        #     vector_store=self._vector_store,
        # )

        # ---------------------------------------------------------
        # Return
        # ---------------------------------------------------------

        return document, chunks