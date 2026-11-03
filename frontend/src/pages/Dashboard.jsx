import { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Database,
  MessageSquare,
  BarChart3,
  FileText,
  Upload,
  Cpu,
  Sparkles,
  ArrowRight,
  TrendingUp,
  FileCheck,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  ChevronRight,
  RefreshCw,
} from "lucide-react";
import {
  getKnowledgeBase,
  uploadDocument,
  checkHealth,
  getSavedReports,
} from "../services/api";

const quickPrompts = [
  {
    target: "/analysis",
    title: "Comparative Performance",
    query: "Compare the revenue and operating margin performance of different business segments.",
    tag: "Comparative",
    color: "#3b82f6",
  },
  {
    target: "/analysis",
    title: "Executive SWOT Analysis",
    query: "Identify key business strengths, operational weaknesses, market opportunities, and potential threats.",
    tag: "SWOT",
    color: "#8b5cf6",
  },
  {
    target: "/chat",
    title: "Risk & Debt Covenants",
    query: "What are the major business risks, debt obligations, and financial covenants noted in the documents?",
    tag: "Risk Audit",
    color: "#f59e0b",
  },
  {
    target: "/analysis",
    title: "Cost & Cash Flow Drivers",
    query: "Analyze the primary drivers behind recent changes in operating cash flows and cost structure.",
    tag: "Root Cause",
    color: "#10b981",
  },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [documents, setDocuments] = useState([]);
  const [totalDocs, setTotalDocs] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [backendHealth, setBackendHealth] = useState(null);
  const [savedReportsCount, setSavedReportsCount] = useState(0);
  const [alert, setAlert] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [health, kb] = await Promise.all([
        checkHealth(),
        getKnowledgeBase().catch(() => ({ documents: [], total_documents: 0 })),
      ]);

      setBackendHealth(health?.status === "healthy");
      const docs = kb?.documents || [];
      setDocuments(docs);
      setTotalDocs(kb?.total_documents ?? docs.length);

      const calculatedPages = docs.reduce(
        (sum, doc) => sum + (doc.total_pages || 0),
        0
      );
      setTotalPages(calculatedPages);

      const reports = getSavedReports();
      setSavedReportsCount(reports.length);
    } catch (err) {
      console.error(err);
      setBackendHealth(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setAlert({ type: "danger", message: "Only PDF documents are supported." });
      return;
    }

    try {
      setUploading(true);
      setAlert(null);
      const res = await uploadDocument(file);
      setAlert({
        type: "success",
        message: `Successfully ingested "${file.name}". Processed ${res.pages} pages into ${res.chunks_created} semantic chunks.`,
      });
      await loadData();
    } catch (err) {
      setAlert({
        type: "danger",
        message: err.message || "Failed to upload and ingest document.",
      });
    } finally {
      setUploading(false);
    }
  };

  const handlePromptClick = (target, query) => {
    navigate(target, { state: { prefilledQuery: query } });
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
      {/* GREETING & STATUS BANNER */}
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
          <h2 style={{ fontSize: "24px", fontWeight: "800", color: "#0f172a", letterSpacing: "-0.02em" }}>
            Workspace Intelligence Center
          </h2>
          <p style={{ color: "#64748b", fontSize: "14px", marginTop: "4px" }}>
            Grounded AI business analysis, hybrid document retrieval, and evidence synthesis.
          </p>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            onClick={loadData}
            className="btn btn-secondary btn-sm"
            disabled={loading}
            title="Refresh workspace status"
          >
            <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            <span>Refresh</span>
          </button>

          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn btn-primary btn-sm"
            disabled={uploading}
          >
            <Upload size={14} />
            <span>{uploading ? "Ingesting PDF..." : "Upload PDF"}</span>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            hidden
            onChange={handleUpload}
          />
        </div>
      </div>

      {/* NOTIFICATIONS */}
      {alert && (
        <div
          style={{
            padding: "12px 18px",
            borderRadius: "10px",
            marginBottom: "20px",
            fontSize: "13.5px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: alert.type === "success" ? "#ecfdf5" : "#fef2f2",
            color: alert.type === "success" ? "#065f46" : "#991b1b",
            border: `1px solid ${alert.type === "success" ? "#a7f3d0" : "#fecaca"}`,
          }}
        >
          {alert.type === "success" ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
          <span>{alert.message}</span>
        </div>
      )}

      {/* KPI METRIC CARDS */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "16px",
          marginBottom: "28px",
        }}
      >
        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
            <span style={{ fontSize: "12px", fontWeight: "700", color: "#64748b", textTransform: "uppercase" }}>
              Indexed Documents
            </span>
            <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "#eff6ff", color: "#2563eb", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Database size={16} />
            </div>
          </div>
          <div style={{ fontSize: "28px", fontWeight: "800", color: "#0f172a" }}>
            {loading ? "..." : totalDocs}
          </div>
          <span style={{ fontSize: "12px", color: "#64748b" }}>
            PDF files ready for hybrid search
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
            <span style={{ fontSize: "12px", fontWeight: "700", color: "#64748b", textTransform: "uppercase" }}>
              Total Processed Pages
            </span>
            <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "#f5f3ff", color: "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <FileCheck size={16} />
            </div>
          </div>
          <div style={{ fontSize: "28px", fontWeight: "800", color: "#0f172a" }}>
            {loading ? "..." : totalPages}
          </div>
          <span style={{ fontSize: "12px", color: "#64748b" }}>
            Docling hierarchical extraction
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
            <span style={{ fontSize: "12px", fontWeight: "700", color: "#64748b", textTransform: "uppercase" }}>
              Retrieval Pipeline
            </span>
            <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "#ecfdf5", color: "#059669", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Layers size={16} />
            </div>
          </div>
          <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a", marginTop: "6px" }}>
            FAISS + BM25
          </div>
          <span style={{ fontSize: "12px", color: "#059669", fontWeight: "600" }}>
            Cross-Encoder Rerank Active
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
            <span style={{ fontSize: "12px", fontWeight: "700", color: "#64748b", textTransform: "uppercase" }}>
              Backend RAG API
            </span>
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "8px",
                background: backendHealth ? "#ecfdf5" : "#fffbeb",
                color: backendHealth ? "#059669" : "#d97706",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Cpu size={16} />
            </div>
          </div>
          <div style={{ fontSize: "20px", fontWeight: "800", color: backendHealth ? "#059669" : "#d97706" }}>
            {backendHealth ? "Online · Port 8000" : "Offline"}
          </div>
          <span style={{ fontSize: "12px", color: "#64748b" }}>
            {backendHealth ? "FastAPI service responding" : "Run: uvicorn app.main:app"}
          </span>
        </div>
      </div>

      {/* PRIMARY WORKSPACE HUBS */}
      <div style={{ marginBottom: "32px" }}>
        <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#1e293b", marginBottom: "14px" }}>
          Intelligence Modules
        </h3>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "16px",
          }}
        >
          {/* Business Analysis Hub */}
          <Link
            to="/analysis"
            className="card"
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              textDecoration: "none",
              borderLeft: "4px solid #2563eb",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <div style={{ width: "36px", height: "36px", borderRadius: "10px", background: "#eff6ff", color: "#2563eb", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <BarChart3 size={20} />
                </div>
                <div>
                  <h4 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>Business Analysis Studio</h4>
                  <span style={{ fontSize: "12px", color: "#64748b" }}>SWOT, Comparative, Trend & Root Cause</span>
                </div>
              </div>
              <p style={{ fontSize: "13px", color: "#475569", lineHeight: "1.5" }}>
                Execute domain-specific analysis models with structured key findings, executive conclusions, and supporting citations.
              </p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#2563eb", fontSize: "13px", fontWeight: "600", marginTop: "16px" }}>
              <span>Open Studio</span>
              <ArrowRight size={14} />
            </div>
          </Link>

          {/* AI Chat Hub */}
          <Link
            to="/chat"
            className="card"
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              textDecoration: "none",
              borderLeft: "4px solid #7c3aed",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <div style={{ width: "36px", height: "36px", borderRadius: "10px", background: "#f5f3ff", color: "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <MessageSquare size={20} />
                </div>
                <div>
                  <h4 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>AI Assistant Chat</h4>
                  <span style={{ fontSize: "12px", color: "#64748b" }}>Interactive Document Interrogation</span>
                </div>
              </div>
              <p style={{ fontSize: "13px", color: "#475569", lineHeight: "1.5" }}>
                Ask natural-language questions across indexed filings with real-time inspection of rerank scores and token usage.
              </p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#7c3aed", fontSize: "13px", fontWeight: "600", marginTop: "16px" }}>
              <span>Start Conversation</span>
              <ArrowRight size={14} />
            </div>
          </Link>

          {/* Knowledge Base Hub */}
          <Link
            to="/knowledge-base"
            className="card"
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              textDecoration: "none",
              borderLeft: "4px solid #059669",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <div style={{ width: "36px", height: "36px", borderRadius: "10px", background: "#ecfdf5", color: "#059669", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Database size={20} />
                </div>
                <div>
                  <h4 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>Document Knowledge Base</h4>
                  <span style={{ fontSize: "12px", color: "#64748b" }}>{totalDocs} Active Document{totalDocs === 1 ? "" : "s"}</span>
                </div>
              </div>
              <p style={{ fontSize: "13px", color: "#475569", lineHeight: "1.5" }}>
                Upload new PDFs, review document metadata, manage indexed chunks, and inspect parsing status.
              </p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#059669", fontSize: "13px", fontWeight: "600", marginTop: "16px" }}>
              <span>Manage Documents</span>
              <ArrowRight size={14} />
            </div>
          </Link>

          {/* Executive Reports Hub */}
          <Link
            to="/reports"
            className="card"
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              textDecoration: "none",
              borderLeft: "4px solid #d97706",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <div style={{ width: "36px", height: "36px", borderRadius: "10px", background: "#fffbeb", color: "#d97706", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <FileText size={20} />
                </div>
                <div>
                  <h4 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>Executive Reports</h4>
                  <span style={{ fontSize: "12px", color: "#64748b" }}>{savedReportsCount} Dossier{savedReportsCount === 1 ? "" : "s"} Saved</span>
                </div>
              </div>
              <p style={{ fontSize: "13px", color: "#475569", lineHeight: "1.5" }}>
                View, filter, and export generated business findings, SWOT matrices, and citations to Markdown and JSON.
              </p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#d97706", fontSize: "13px", fontWeight: "600", marginTop: "16px" }}>
              <span>Browse Saved Reports</span>
              <ArrowRight size={14} />
            </div>
          </Link>
        </div>
      </div>

      {/* QUICK LAUNCH PROMPT TEMPLATES */}
      <div style={{ marginBottom: "32px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
          <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#1e293b" }}>
            Recommended Business Analyst Interrogations
          </h3>
          <span style={{ fontSize: "12px", color: "#64748b" }}>
            Click to launch studio with prefilled question
          </span>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: "14px",
          }}
        >
          {quickPrompts.map((item, idx) => (
            <div
              key={idx}
              className="card"
              onClick={() => handlePromptClick(item.target, item.query)}
              style={{
                padding: "16px",
                cursor: "pointer",
                transition: "all 0.2s",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
              }}
            >
              <div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                  <span
                    style={{
                      fontSize: "11px",
                      fontWeight: "700",
                      color: item.color,
                      textTransform: "uppercase",
                      letterSpacing: "0.04em",
                    }}
                  >
                    {item.tag}
                  </span>
                  <Sparkles size={14} color={item.color} />
                </div>
                <h4 style={{ fontSize: "14px", fontWeight: "700", color: "#0f172a", marginBottom: "6px" }}>
                  {item.title}
                </h4>
                <p style={{ fontSize: "12.5px", color: "#64748b", lineHeight: "1.4" }}>
                  "{item.query}"
                </p>
              </div>

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "flex-end",
                  color: "#2563eb",
                  fontSize: "12px",
                  fontWeight: "600",
                  marginTop: "12px",
                }}
              >
                <span>Run Analysis</span>
                <ChevronRight size={14} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* RECENT DOCUMENTS OVERVIEW */}
      <div className="card" style={{ padding: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "18px" }}>
          <div>
            <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>
              Knowledge Base Index
            </h3>
            <p style={{ fontSize: "12.5px", color: "#64748b", marginTop: "2px" }}>
              Active PDF documents currently available to the hybrid RAG engine
            </p>
          </div>

          <Link to="/knowledge-base" className="btn btn-secondary btn-sm">
            <span>View All Documents</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        {loading ? (
          <div style={{ textAlign: "center", padding: "30px", color: "#94a3b8" }}>
            Loading indexed documents...
          </div>
        ) : documents.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              padding: "40px 20px",
              background: "#f8fafc",
              borderRadius: "12px",
              border: "1px dashed #cbd5e1",
            }}
          >
            <Database size={32} color="#94a3b8" style={{ margin: "0 auto 12px" }} />
            <h4 style={{ fontSize: "15px", fontWeight: "700", color: "#334155" }}>
              No documents indexed yet
            </h4>
            <p style={{ fontSize: "13px", color: "#64748b", maxWidth: "420px", margin: "6px auto 18px" }}>
              Upload your first annual report, financial deck, or operational document to begin querying.
            </p>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn btn-primary btn-sm"
              disabled={uploading}
            >
              <Upload size={14} />
              <span>Upload PDF Document</span>
            </button>
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13.5px" }}>
              <thead>
                <tr style={{ borderBottom: "1px solid #e2e8f0", textAlign: "left", color: "#64748b", fontSize: "12px" }}>
                  <th style={{ padding: "10px 12px", fontWeight: "600" }}>DOCUMENT NAME</th>
                  <th style={{ padding: "10px 12px", fontWeight: "600" }}>PAGES</th>
                  <th style={{ padding: "10px 12px", fontWeight: "600" }}>FORMAT</th>
                  <th style={{ padding: "10px 12px", fontWeight: "600" }}>INDEX STATUS</th>
                </tr>
              </thead>
              <tbody>
                {documents.slice(0, 5).map((doc) => (
                  <tr key={doc.document_id} style={{ borderBottom: "1px solid #f1f5f9" }}>
                    <td style={{ padding: "12px", color: "#0f172a", fontWeight: "600" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <span style={{ padding: "2px 6px", background: "#fee2e2", color: "#dc2626", borderRadius: "4px", fontSize: "10px", fontWeight: "700" }}>
                          PDF
                        </span>
                        <span>{doc.document_name || doc.title || "Unnamed Document"}</span>
                      </div>
                    </td>
                    <td style={{ padding: "12px", color: "#64748b" }}>
                      {doc.total_pages || 1} pages
                    </td>
                    <td style={{ padding: "12px", color: "#64748b" }}>
                      {doc.file_type || "PDF"}
                    </td>
                    <td style={{ padding: "12px" }}>
                      <span className="badge badge-success">
                        <CheckCircle2 size={11} />
                        <span>Indexed (FAISS + BM25)</span>
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
