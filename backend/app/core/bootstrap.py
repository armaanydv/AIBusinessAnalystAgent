from app.document.chunking.chunk_builder import ChunkBuilder
from app.document.hierarchy.hierarchy_builder import HierarchyBuilder
from app.document.indexing.index_builder import IndexBuilder
from app.document.relationships.relationship_builder import RelationshipBuilder
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.parsers.docling_parser import DoclingParser
from app.preprocessing.document_preprocessor import DocumentPreprocessor
from app.retrieval.embeddings.bge_embedding_model import BGEEmbeddingModel
from app.retrieval.embeddings.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store.faiss_vector_store import FAISSVectorStore
from app.storage.artifact_storage import ArtifactStorage

# ==========================================================
# Core Components
# ==========================================================

parser = DoclingParser()

preprocessor = DocumentPreprocessor()

index_builder = IndexBuilder()

relationship_builder = RelationshipBuilder()

hierarchy_builder = HierarchyBuilder()

chunk_builder = ChunkBuilder()

# ==========================================================
# Retrieval Components
# ==========================================================

embedding_model = BGEEmbeddingModel()

embedding_generator = EmbeddingGenerator(
    embedding_model=embedding_model,
)

vector_store = FAISSVectorStore(
    dimension=embedding_model.dimension,
)

# ==========================================================
# Storage
# ==========================================================

artifact_storage = ArtifactStorage()

# ==========================================================
# Services
# ==========================================================

ingestion_service = IngestionService(
    parser=parser,
    preprocessor=preprocessor,
    index_builder=index_builder,
    relationship_builder=relationship_builder,
    hierarchy_builder=hierarchy_builder,
    chunk_builder=chunk_builder,
    embedding_generator=embedding_generator,
    vector_store=vector_store,
    artifact_storage=artifact_storage,
)