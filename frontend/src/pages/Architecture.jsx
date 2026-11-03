import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Cpu,
  Database,
  Layers,
  Search,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  FileCode,
  Activity,
  FileText,
  Shield,
  Zap,
} from "lucide-react";
import { checkHealth, getApiBaseUrl } from "../services/api";

const pipelineStages = [
  {
    step: "01",
    name: "Docling PDF Parsing",
    badge: "Structural Ingestion",
    color: "#3b82f6",
    summary:
      "Deep document parsing preserving multi-column layouts, tabular structures, and section hierarchies into structured JSON representations.",
    details:
      "Instead of dumb OCR or linear text extraction, Docling identifies document semantics (tables, headers, footnotes, callout boxes). This preserves critical financial statement relationships.",
  },
  {
    step: "02",
    name: "Document Hierarchy Mapping",
    badge: "Semantic Modeling",
    color: "#6366f1",
    summary:
      "Constructs an explicit structural tree of sections, subsections, tables, and narrative paragraphs.",
    details:
      "Retains contextual parents and metadata so chunks never lose their parent section heading or reporting period.",
  },
  {
    step: "03",
    name: "Semantic Chunking",
    badge: "Context Preservation",
    color: "#8b5cf6",
    summary:
      "Partitions documents into semantically coherent chunk boundaries rather than arbitrary character splits.",
    details:
      "Ensures financial disclosures, tables, and qualitative risks remain intact within unified retrieval blocks.",
  },
  {
    step: "04",
    name: "BGE Embedding & FAISS Indexing",
    badge: "Dense Semantic Vector",
    color: "#06b6d4",
    summary:
      "Computes dense embeddings via BGE model and populates a FAISS inner-product index configured for cosine similarity.",
    details:
      "Allows the retrieval system to match conceptual questions (e.g., 'liquidity risks') even when exact words differ in the filing.",
  },
  {
    step: "05",
    name: "BM25 Keyword Indexing",
    badge: "Sparse Lexical Search",
    color: "#10b981",
    summary:
      "Maintains an inverted BM25 index over chunk tokens to ensure pinpoint accuracy for financial metrics, tickers, and names.",
    details:
      "Guarantees that queries containing specific entity names, GAAP codes, or dollar values ($42.5M) are retrieved reliably.",
  },
  {
    step: "06",
    name: "Reciprocal Rank Fusion (RRF)",
    badge: "Hybrid Score Merge",
    color: "#f59e0b",
    summary:
      "Fuses the dense semantic rankings from FAISS with sparse lexical rankings from BM25 using RRF.",
    details:
      "Mitigates the blind spots of pure vector search while avoiding score scale mismatch between cosine and BM25 scores.",
  },
  {
    step: "07",
    name: "Cross-Encoder Precision Reranking",
    badge: "Relevance Scoring",
    color: "#ec4899",
    summary:
      "Top hybrid candidates are passed to a cross-encoder model that scores query-document relevance jointly.",
    details:
      "Yields normalized reranking scores (0.0 to 1.0). Evidence below confidence thresholds is pruned, dramatically cutting hallucinations.",
  },
  {
    step: "08",
    name: "Business Analyst LLM Synthesis",
    badge: "Structured Reasoning",
    color: "#14b8a6",
    summary:
      "Domain-specific prompts instruct the configured LLM to generate structured key findings, executive conclusions, and citations.",
    details:
      "Validates outputs against strict schemas: SWOT matrices, comparative tables, and itemized conclusions tied to chunk IDs.",
  },
];

const apiEndpoints = [
  {
    method: "GET",
    path: "/health",
    desc: "Health check and service status verification",
  },
  {
    method: "GET",
    path: "/knowledge-base",
    desc: "List all indexed PDF documents, pages, and metadata",
  },
  {
    method: "POST",
    path: "/upload",
    desc: "Upload and ingest PDF via Docling into FAISS & BM25",
  },
  {
    method: "DELETE",
    path: "/knowledge-base/{id}",
    desc: "Remove document and purge vectors from index",
  },
  {
    method: "POST",
    path: "/chat",
    desc: "Submit query for hybrid retrieval, reranking, and LLM answer",
  },
  {
    method: "POST",
    path: "/analysis",
    desc: "Execute business analysis models (SWOT, Comparative, Trend)",
  },
];

export default function Architecture() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [latency, setLatency] = useState(null);
  const [testingHealth, setTestingHealth] = useState(false);
  const [activeStage, setActiveStage] = useState(0);

  const testApiHealth = async () => {
    setTestingHealth(true);
    const start = performance.now();
    try {
      const res = await checkHealth();
      const end = performance.now();
      setLatency(Math.round(end - start));
      setHealthStatus(res?.status === "healthy" ? "healthy" : "offline");
    } catch {
      setHealthStatus("offline");
      setLatency(null);
    } finally {
      setTestingHealth(false);
    }
  };

  useEffect(() => {
    testApiHealth();
  }, []);

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "16px",
          marginBottom: "28px",
        }}
      >
        <div>
          <h2 style={{ fontSize: "24px", fontWeight: "800", color: "#0f172a" }}>
            RAG Architecture & Methodology
          </h2>
          <p style={{ color: "#64748b", fontSize: "14px", marginTop: "4px" }}>
            Under the hood: deep PDF structural parsing, hybrid vector + lexical search, and cross-encoder reranking.
          </p>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <button
            onClick={testApiHealth}
            className="btn btn-secondary btn-sm"
            disabled={testingHealth}
          >
            <Activity size={14} className={testingHealth ? "animate-spin" : ""} />
            <span>{testingHealth ? "Testing API..." : "Ping Backend"}</span>
          </button>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="btn btn-primary btn-sm"
          >
            <FileCode size={14} />
            <span>Open Swagger Docs</span>
          </a>
        </div>
      </div>

      {/* HEALTH STATUS CARD */}
      <div
        className="card"
        style={{
          padding: "18px 24px",
          marginBottom: "28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: "16px",
          background: healthStatus === "healthy" ? "#f0fdf4" : "#fffbeb",
          borderColor: healthStatus === "healthy" ? "#bbf7d0" : "#fef3c7",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
          <div
            style={{
              width: "40px",
              height: "40px",
              borderRadius: "10px",
              background: healthStatus === "healthy" ? "#dcfce7" : "#fef3c7",
              color: healthStatus === "healthy" ? "#16a34a" : "#d97706",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {healthStatus === "healthy" ? <CheckCircle2 size={22} /> : <AlertCircle size={22} />}
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#0f172a", margin: 0 }}>
                {healthStatus === "healthy" ? "FastAPI RAG Backend Online" : "Local Backend Offline / Connecting"}
              </h4>
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: "700",
                  padding: "2px 8px",
                  borderRadius: "999px",
                  background: healthStatus === "healthy" ? "#16a34a" : "#d97706",
                  color: "#fff",
                }}
              >
                {healthStatus === "healthy" ? "200 OK" : "Port 8000"}
              </span>
            </div>
            <p style={{ fontSize: "12.5px", color: "#475569", margin: "2px 0 0" }}>
              Target endpoint: <code>{getApiBaseUrl()}</code>
              {latency !== null && ` · Ping Latency: ${latency}ms`}
            </p>
          </div>
        </div>

        <Link to="/settings" className="btn btn-secondary btn-sm" style={{ background: "#fff" }}>
          <span>Configure Endpoint</span>
          <ArrowRight size={13} />
        </Link>
      </div>

      {/* PIPELINE STAGES EXPLORER */}
      <div style={{ marginBottom: "36px" }}>
        <h3 style={{ fontSize: "18px", fontWeight: "700", color: "#0f172a", marginBottom: "6px" }}>
          The 8-Stage Document Intelligence Pipeline
        </h3>
        <p style={{ color: "#64748b", fontSize: "13.5px", marginBottom: "18px" }}>
          Click any stage below to inspect its purpose, algorithms, and hallucination safeguards.
        </p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "12px", marginBottom: "20px" }}>
          {pipelineStages.map((stg, idx) => (
            <div
              key={stg.step}
              onClick={() => setActiveStage(idx)}
              className="card"
              style={{
                padding: "16px",
                cursor: "pointer",
                borderLeft: `4px solid ${stg.color}`,
                background: activeStage === idx ? "#f8fafc" : "#fff",
                borderColor: activeStage === idx ? stg.color : "#e2e8f0",
                boxShadow: activeStage === idx ? "0 4px 12px rgba(0,0,0,0.06)" : "none",
                transition: "all 0.2s",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ fontSize: "11px", fontFamily: "var(--font-mono)", fontWeight: "700", color: stg.color }}>
                  STAGE {stg.step}
                </span>
                <span style={{ fontSize: "10px", padding: "1px 6px", borderRadius: "4px", background: "#f1f5f9", color: "#64748b", fontWeight: "600" }}>
                  {stg.badge}
                </span>
              </div>
              <h4 style={{ fontSize: "13.5px", fontWeight: "700", color: "#0f172a" }}>
                {stg.name}
              </h4>
            </div>
          ))}
        </div>

        {/* ACTIVE STAGE DETAIL CARD */}
        <div
          className="card"
          style={{
            padding: "26px",
            borderLeft: `5px solid ${pipelineStages[activeStage].color}`,
            background: "#fff",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
            <div>
              <span
                style={{
                  fontSize: "12px",
                  fontWeight: "700",
                  color: pipelineStages[activeStage].color,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                }}
              >
                Stage {pipelineStages[activeStage].step} Detail
              </span>
              <h3 style={{ fontSize: "20px", fontWeight: "800", color: "#0f172a", marginTop: "2px" }}>
                {pipelineStages[activeStage].name}
              </h3>
            </div>
            <span className="badge" style={{ background: "#f1f5f9", color: "#475569", fontSize: "12px" }}>
              {pipelineStages[activeStage].badge}
            </span>
          </div>

          <p style={{ fontSize: "14.5px", color: "#334155", lineHeight: "1.6", marginBottom: "16px" }}>
            {pipelineStages[activeStage].summary}
          </p>

          <div
            style={{
              padding: "16px",
              background: "#f8fafc",
              borderRadius: "10px",
              border: "1px solid #e2e8f0",
              fontSize: "13.5px",
              color: "#475569",
              lineHeight: "1.6",
            }}
          >
            <strong style={{ color: "#0f172a", display: "block", marginBottom: "4px" }}>
              Why this matters for business analysis:
            </strong>
            {pipelineStages[activeStage].details}
          </div>
        </div>
      </div>

      {/* ARCHITECTURAL COMPARISON */}
      <div style={{ marginBottom: "36px" }}>
        <h3 style={{ fontSize: "18px", fontWeight: "700", color: "#0f172a", marginBottom: "16px" }}>
          Standard Naive RAG vs AIBA Enterprise Architecture
        </h3>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          <div className="card" style={{ padding: "20px", background: "#fef2f2", borderColor: "#fecaca" }}>
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#991b1b", marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
              <AlertCircle size={16} />
              <span>Standard Naive RAG Wrappers</span>
            </h4>
            <ul style={{ paddingLeft: "18px", fontSize: "13px", color: "#7f1d1d", display: "flex", flexDirection: "column", gap: "8px", lineHeight: "1.5" }}>
              <li>Splits text by arbitrary character count (e.g. 500 chars), chopping financial tables in half.</li>
              <li>Pure vector cosine search fails to match exact GAAP items, dates, and currency values.</li>
              <li>No cross-encoder reranking: irrelevant chunks clutter the context, prompting LLM hallucinations.</li>
              <li>Returns unstructured text without source line references or evidence confidence scores.</li>
            </ul>
          </div>

          <div className="card" style={{ padding: "20px", background: "#f0fdf4", borderColor: "#bbf7d0" }}>
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#166534", marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
              <CheckCircle2 size={16} />
              <span>AIBA Hybrid RAG Engine</span>
            </h4>
            <ul style={{ paddingLeft: "18px", fontSize: "13px", color: "#14532d", display: "flex", flexDirection: "column", gap: "8px", lineHeight: "1.5" }}>
              <li>Docling deep parsing preserves entire balance sheets, nested tables, and heading structures.</li>
              <li>Hybrid Vector (FAISS) + Lexical (BM25) fusion guarantees both conceptual and literal recall.</li>
              <li>Cross-encoder reranking filters low-confidence noise before prompt construction.</li>
              <li>Outputs structured findings with chunk-level attribution, rerank scores, and token diagnostics.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* REST API ENDPOINTS TABLE */}
      <div className="card" style={{ padding: "24px" }}>
        <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a", marginBottom: "6px" }}>
          FastAPI Backend Endpoints
        </h3>
        <p style={{ fontSize: "13px", color: "#64748b", marginBottom: "18px" }}>
          Authoritative endpoints implemented in <code>backend/app/api</code>
        </p>

        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13.5px" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #e2e8f0", textAlign: "left", color: "#64748b", fontSize: "12px" }}>
                <th style={{ padding: "10px 12px", width: "100px" }}>METHOD</th>
                <th style={{ padding: "10px 12px", width: "240px" }}>ENDPOINT</th>
                <th style={{ padding: "10px 12px" }}>FUNCTION & PURPOSE</th>
              </tr>
            </thead>
            <tbody>
              {apiEndpoints.map((ep, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #f1f5f9" }}>
                  <td style={{ padding: "12px" }}>
                    <span
                      style={{
                        padding: "3px 8px",
                        borderRadius: "4px",
                        fontSize: "11px",
                        fontWeight: "700",
                        fontFamily: "var(--font-mono)",
                        background: ep.method === "GET" ? "#eff6ff" : ep.method === "POST" ? "#ecfdf5" : "#fef2f2",
                        color: ep.method === "GET" ? "#2563eb" : ep.method === "POST" ? "#059669" : "#dc2626",
                      }}
                    >
                      {ep.method}
                    </span>
                  </td>
                  <td style={{ padding: "12px", fontFamily: "var(--font-mono)", fontSize: "13px", color: "#0f172a", fontWeight: "600" }}>
                    {ep.path}
                  </td>
                  <td style={{ padding: "12px", color: "#475569" }}>
                    {ep.desc}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
