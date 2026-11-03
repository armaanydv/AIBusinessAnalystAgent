import { useLocation, Link, useNavigate } from "react-router-dom";
import {
  Upload,
  Sparkles,
  HelpCircle,
  FileText,
  Search,
} from "lucide-react";

const pageDetails = {
  "/dashboard": {
    title: "Executive Dashboard",
    description: "Real-time overview of document intelligence, active indices, and quick actions.",
  },
  "/chat": {
    title: "AI Business Assistant",
    description: "Multi-turn RAG chat with grounded document citations and reranking metrics.",
  },
  "/knowledge-base": {
    title: "Document Knowledge Base",
    description: "Manage, ingest, and inspect PDF business documents indexed in FAISS and BM25.",
  },
  "/analysis": {
    title: "Business Analysis Studio",
    description: "Deep structured business intelligence: SWOT, comparative, root cause, and trends.",
  },
  "/reports": {
    title: "Executive Reports",
    description: "Review, search, and export saved business analysis dossiers and strategic findings.",
  },
  "/methodology": {
    title: "RAG Architecture & Pipeline",
    description: "Inspect the Docling parsing, hybrid FAISS + BM25 retrieval, and cross-encoder reranking.",
  },
  "/settings": {
    title: "Workspace Settings",
    description: "Manage backend connectivity, retrieval parameters, and local data persistence.",
  },
};

export default function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  const currentInfo = pageDetails[location.pathname] || {
    title: "AIBA Workspace",
    description: "Evidence-backed business analysis powered by AI.",
  };

  return (
    <header className="app-header">
      <div className="header-breadcrumbs">
        <div>
          <h1 style={{ fontSize: "19px", fontWeight: "700", color: "#0f172a", letterSpacing: "-0.01em" }}>
            {currentInfo.title}
          </h1>
          <p style={{ fontSize: "12.5px", color: "#64748b", marginTop: "2px" }}>
            {currentInfo.description}
          </p>
        </div>
      </div>

      <div className="header-actions">
        {location.pathname !== "/knowledge-base" && (
          <button
            onClick={() => navigate("/knowledge-base")}
            className="btn btn-secondary btn-sm"
            title="Upload new PDF document"
          >
            <Upload size={14} />
            <span>Upload Document</span>
          </button>
        )}

        <Link
          to="/methodology"
          className="header-pill"
          title="Inspect RAG Architecture"
          style={{ textDecoration: "none" }}
        >
          <Sparkles size={14} color="#6366f1" />
          <span>Hybrid RAG Engine</span>
        </Link>
      </div>
    </header>
  );
}
