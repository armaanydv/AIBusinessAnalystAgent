from app.document.chunking.chunk_builder import ChunkBuilder
from app.document.hierarchy.hierarchy_builder import HierarchyBuilder
from app.document.indexing.index_builder import IndexBuilder
from app.document.relationships.relationship_builder import (
    RelationshipBuilder,
)

from app.ingestion.ingestion_service import IngestionService
from app.ingestion.parsers.docling_parser import DoclingParser

from app.llm.llm_factory import LLMFactory
from app.llm.output_parser import OutputParser

from app.preprocessing.document_preprocessor import (
    DocumentPreprocessor,
)

from app.prompting.rag_prompt_builder import (
    RAGPromptBuilder,
)

from app.services.knowledge_base_service import (
    KnowledgeBaseService,
)
from app.services.rag_service import RAGService

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

from app.storage.artifact_storage import ArtifactStorage

from app.retrieval.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
)
from app.retrieval.reranker.rerank_config import (
    get_reranker_config,
)

from app.analysis.analysis_selector import AnalysisSelector
from app.analysis.analysis_service import AnalysisService
from app.analysis.question_analyzer import QuestionAnalyzer
from app.analysis.retrieval_planner import RetrievalPlanner

from app.analysis.techniques.comparative_analysis import (
    ComparativeAnalysis,
)
from app.analysis.techniques.trend_analysis import (
    TrendAnalysis,
)
from app.analysis.techniques.ranking_analysis import (
    RankingAnalysis,
)
from app.analysis.techniques.root_cause_analysis import (
    RootCauseAnalysis,
)
from app.analysis.techniques.contribution_analysis import (
    ContributionAnalysis,
)
from app.analysis.techniques.swot_analysis import (
    SWOTAnalysis,
)


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
# Embeddings
# ==========================================================

embedding_model = BGEEmbeddingModel()

embedding_generator = EmbeddingGenerator(
    embedding_model=embedding_model,
)


# ==========================================================
# Search Indexes
# ==========================================================

vector_store = FAISSVectorStore(
    dimension=embedding_model.dimension,
)

bm25_tokenizer = BM25Tokenizer()

bm25_config = BM25Config()

bm25_index = BM25Index(
    tokenizer=bm25_tokenizer,
    config=bm25_config,
)


# ==========================================================
# Chunk Repository
# ==========================================================

chunk_repository = ChunkRepository()


# ==========================================================
# Storage
# ==========================================================

artifact_storage = ArtifactStorage()


# ==========================================================
# Knowledge Base Service
# ==========================================================

knowledge_base_service = KnowledgeBaseService(
    artifact_storage=artifact_storage,
    chunk_repository=chunk_repository,
    vector_store=vector_store,
    bm25_index=bm25_index,
)


# ==========================================================
# Restore Persisted Knowledge Base
# ==========================================================

try:

    knowledge_base_service.restore()

    loaded_documents = len(
        artifact_storage.list_documents()
    )

    print(
        f"[INFO] Restored "
        f"{loaded_documents} document(s) "
        f"containing {len(vector_store)} vectors."
    )

except Exception as exc:

    print(
        f"[WARNING] Failed to restore "
        f"Knowledge Base: {exc}"
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

reranker = CrossEncoderReranker(
    config=get_reranker_config(),
)


# ==========================================================
# Prompting
# ==========================================================

prompt_builder = RAGPromptBuilder()


# ==========================================================
# Output Parsing
# ==========================================================

output_parser = OutputParser()


# ==========================================================
# LLM
# ==========================================================

llm = LLMFactory.create()


# ==========================================================
# RAG Service
# ==========================================================

rag_service = RAGService(
    retriever=hybrid_retriever,
    reranker=reranker,
    prompt_builder=prompt_builder,
    llm=llm,
    output_parser=output_parser,
)


# ==========================================================
# Question Analysis
# ==========================================================

question_analyzer = QuestionAnalyzer(
    llm=llm,
)


# ==========================================================
# Retrieval Planning
# ==========================================================

retrieval_planner = RetrievalPlanner()


# ==========================================================
# Analysis Techniques
# ==========================================================

comparative_analysis = ComparativeAnalysis(
    llm=llm,
)

trend_analysis = TrendAnalysis(
    llm=llm,
)

ranking_analysis = RankingAnalysis(
    llm=llm,
)

root_cause_analysis = RootCauseAnalysis(
    llm=llm,
)

contribution_analysis = ContributionAnalysis(
    llm=llm,
)

swot_analysis = SWOTAnalysis(
    llm=llm,
)


# ==========================================================
# Analysis Selector
# ==========================================================

analysis_selector = AnalysisSelector(
    analyses={
        "comparative": comparative_analysis,
        "trend": trend_analysis,
        "ranking": ranking_analysis,
        "root_cause": root_cause_analysis,
        "contribution": contribution_analysis,
        "swot": swot_analysis,
    }
)


# ==========================================================
# Analysis Service
# ==========================================================

analysis_service = AnalysisService(
    question_analyzer=question_analyzer,
    retrieval_planner=retrieval_planner,
    rag_service=rag_service,
    analysis_selector=analysis_selector,
)


# ==========================================================
# Ingestion Service
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
    bm25_index=bm25_index,
    chunk_repository=chunk_repository,
    artifact_storage=artifact_storage,
)