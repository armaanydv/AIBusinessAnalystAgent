import { useCallback, useEffect, useRef, useState } from "react";
import {
  Upload,
  Database,
  Search,
  LayoutGrid,
  List,
  Trash2,
  RefreshCw,
  FileCheck,
  CheckCircle2,
  AlertCircle,
  FileText,
  Calendar,
  Layers,
} from "lucide-react";
import {
  getKnowledgeBase,
  uploadDocument,
  deleteDocument,
} from "../services/api";
import ConfirmModal from "../components/ui/ConfirmModal";
import "./knowledge-base.css";

function formatDate(dateString) {
  if (!dateString) return "—";
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return dateString;
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function KnowledgeBase() {
  const [documents, setDocuments] = useState([]);
  const [totalDocuments, setTotalDocuments] = useState(0);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState("grid"); // 'grid' | 'table'
  const [isDragOver, setIsDragOver] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [docToDelete, setDocToDelete] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const fileInputRef = useRef(null);

  const loadDocuments = useCallback(async () => {
    try {
      setError("");
      setLoading(true);
      const data = await getKnowledgeBase();
      setDocuments(data.documents || []);
      setTotalDocuments(data.total_documents ?? (data.documents || []).length);
    } catch (err) {
      setError(
        err.message ||
          "Unable to load Knowledge Base. Ensure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const processUpload = async (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported for document indexing.");
      setSuccess("");
      return;
    }

    try {
      setUploading(true);
      setError("");
      setSuccess("");

      const result = await uploadDocument(file);
      setSuccess(
        `Successfully ingested "${file.name}". Processed ${result.pages} pages into ${result.chunks_created} semantic chunks.`
      );
      await loadDocuments();
    } catch (err) {
      setError(err.message || "Document upload and ingestion failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (file) processUpload(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) processUpload(file);
  };

  const promptDelete = (doc) => {
    setDocToDelete(doc);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (!docToDelete) return;
    try {
      setIsDeleting(true);
      setError("");
      setSuccess("");

      await deleteDocument(docToDelete.document_id);
      setSuccess(`"${docToDelete.document_name}" was successfully removed from the index.`);
      await loadDocuments();
    } catch (err) {
      setError(err.message || "Unable to delete document from knowledge base.");
    } finally {
      setIsDeleting(false);
      setIsDeleteModalOpen(false);
      setDocToDelete(null);
    }
  };

  // Filter documents by search query
  const filteredDocs = documents.filter((doc) => {
    const q = searchQuery.toLowerCase();
    const nameMatch = doc.document_name && doc.document_name.toLowerCase().includes(q);
    const titleMatch = doc.title && doc.title.toLowerCase().includes(q);
    return nameMatch || titleMatch;
  });

  const totalPagesSum = documents.reduce((acc, d) => acc + (d.total_pages || 0), 0);

  return (
    <div className="kb-page">
      {/* HEADER */}
      <div className="kb-top-bar">
        <div>
          <h2>Document Knowledge Base</h2>
          <p>
            Upload and manage the business filings, annual reports, and decks indexing into FAISS and BM25.
          </p>
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          <button
            onClick={loadDocuments}
            className="btn btn-secondary btn-sm"
            disabled={loading || uploading}
          >
            <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            <span>Refresh Index</span>
          </button>

          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn btn-primary btn-sm"
            disabled={uploading}
          >
            <Upload size={14} />
            <span>{uploading ? "Ingesting..." : "Upload PDF"}</span>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            hidden
            onChange={handleFileInput}
          />
        </div>
      </div>

      {/* DROPZONE */}
      <div
        className={`kb-dropzone ${isDragOver ? "dragover" : ""}`}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="dropzone-icon-wrap">
          <Upload size={22} />
        </div>
        <h4>Drag & Drop your Business PDF here</h4>
        <p>
          or click to browse files from your computer. Docling will parse hierarchical tables and index chunks for hybrid search.
        </p>
        {uploading && (
          <div style={{ marginTop: "14px", display: "flex", alignItems: "center", gap: "8px", color: "#2563eb", fontWeight: "600", fontSize: "13px" }}>
            <RefreshCw size={16} className="animate-spin" />
            <span>Parsing layout, building chunks, and embedding vectors...</span>
          </div>
        )}
      </div>

      {/* ALERTS */}
      {success && (
        <div
          style={{
            padding: "14px 18px",
            borderRadius: "10px",
            background: "#ecfdf5",
            border: "1px solid #a7f3d0",
            color: "#065f46",
            fontSize: "13.5px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <CheckCircle2 size={18} style={{ flexShrink: 0 }} />
          <span>{success}</span>
        </div>
      )}

      {error && (
        <div
          style={{
            padding: "14px 18px",
            borderRadius: "10px",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            color: "#991b1b",
            fontSize: "13.5px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <AlertCircle size={18} style={{ flexShrink: 0 }} />
          <span>{error}</span>
        </div>
      )}

      {/* STATS STRIP & FILTER BAR */}
      <div className="kb-filter-row">
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ fontSize: "13.5px", color: "#475569" }}>
            <strong>{totalDocuments}</strong> {totalDocuments === 1 ? "document" : "documents"} indexed
            {totalPagesSum > 0 && ` (${totalPagesSum} total pages)`}
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          <div className="kb-search-box">
            <Search size={16} color="#94a3b8" />
            <input
              type="text"
              placeholder="Filter by document name or title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div style={{ display: "flex", background: "#f1f5f9", borderRadius: "8px", padding: "2px" }}>
            <button
              onClick={() => setViewMode("grid")}
              style={{
                border: "none",
                background: viewMode === "grid" ? "#fff" : "transparent",
                color: viewMode === "grid" ? "#0f172a" : "#64748b",
                borderRadius: "6px",
                padding: "6px 10px",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
              }}
              title="Grid View"
            >
              <LayoutGrid size={15} />
            </button>
            <button
              onClick={() => setViewMode("table")}
              style={{
                border: "none",
                background: viewMode === "table" ? "#fff" : "transparent",
                color: viewMode === "table" ? "#0f172a" : "#64748b",
                borderRadius: "6px",
                padding: "6px 10px",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
              }}
              title="Table View"
            >
              <List size={15} />
            </button>
          </div>
        </div>
      </div>

      {/* DOCUMENTS DISPLAY */}
      {loading ? (
        <div
          className="card"
          style={{ padding: "40px", textAlign: "center", color: "#64748b" }}
        >
          <RefreshCw size={24} className="animate-spin" style={{ margin: "0 auto 12px", color: "#2563eb" }} />
          <p style={{ fontSize: "14px" }}>Loading indexed knowledge base...</p>
        </div>
      ) : documents.length === 0 ? (
        <div
          className="card"
          style={{
            padding: "60px 20px",
            textAlign: "center",
            border: "1px dashed #cbd5e1",
          }}
        >
          <Database size={40} color="#94a3b8" style={{ margin: "0 auto 16px" }} />
          <h3 style={{ fontSize: "18px", fontWeight: "700", color: "#0f172a", marginBottom: "8px" }}>
            Your Knowledge Base is Empty
          </h3>
          <p style={{ color: "#64748b", fontSize: "14px", maxWidth: "460px", margin: "0 auto 20px" }}>
            Upload annual 10-K filings, corporate strategy PDFs, or financial presentations to enable semantic search and business analysis.
          </p>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn btn-primary"
            disabled={uploading}
          >
            <Upload size={15} />
            <span>Upload Your First PDF</span>
          </button>
        </div>
      ) : filteredDocs.length === 0 ? (
        <div className="card" style={{ padding: "36px", textAlign: "center", color: "#64748b" }}>
          <p>No documents found matching "{searchQuery}".</p>
        </div>
      ) : viewMode === "grid" ? (
        <div className="kb-grid">
          {filteredDocs.map((doc) => (
            <div key={doc.document_id} className="doc-card">
              <div>
                <div className="doc-card-header">
                  <div className="pdf-badge-icon">PDF</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <h4 className="doc-card-title">{doc.document_name}</h4>
                    {doc.title && (
                      <span className="doc-card-subtitle">{doc.title}</span>
                    )}
                  </div>
                </div>

                <div className="doc-meta-pills">
                  <span className="meta-pill">
                    <FileText size={12} />
                    <span>{doc.total_pages || 1} pages</span>
                  </span>
                  <span className="meta-pill">
                    <Calendar size={12} />
                    <span>{formatDate(doc.created_at)}</span>
                  </span>
                  <span className="badge badge-success" style={{ fontSize: "10.5px" }}>
                    <CheckCircle2 size={11} />
                    <span>FAISS + BM25</span>
                  </span>
                </div>
              </div>

              <div className="doc-card-actions">
                <span style={{ fontSize: "11px", color: "#94a3b8", fontFamily: "var(--font-mono)" }}>
                  ID: {doc.document_id ? doc.document_id.slice(0, 8) : "—"}...
                </span>

                <button
                  onClick={() => promptDelete(doc)}
                  className="btn btn-ghost btn-sm"
                  style={{ color: "#ef4444", padding: "6px 10px" }}
                  title="Delete from knowledge base"
                >
                  <Trash2 size={14} />
                  <span>Delete</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="kb-table-container">
          <table className="kb-table">
            <thead>
              <tr>
                <th>DOCUMENT NAME</th>
                <th>FILE TYPE</th>
                <th>TOTAL PAGES</th>
                <th>INDEXED DATE</th>
                <th style={{ textAlign: "right" }}>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {filteredDocs.map((doc) => (
                <tr key={doc.document_id}>
                  <td>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                      <span style={{ padding: "2px 6px", background: "#fee2e2", color: "#dc2626", borderRadius: "4px", fontSize: "10.5px", fontWeight: "700" }}>
                        PDF
                      </span>
                      <div>
                        <strong style={{ color: "#0f172a", display: "block" }}>
                          {doc.document_name}
                        </strong>
                        {doc.title && (
                          <span style={{ fontSize: "11.5px", color: "#64748b" }}>
                            {doc.title}
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  <td>{doc.file_type || "PDF"}</td>
                  <td>{doc.total_pages ?? "1"}</td>
                  <td>{formatDate(doc.created_at)}</td>
                  <td style={{ textAlign: "right" }}>
                    <button
                      onClick={() => promptDelete(doc)}
                      className="btn btn-ghost btn-sm"
                      style={{ color: "#ef4444" }}
                    >
                      <Trash2 size={13} />
                      <span>Delete</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* CONFIRM DELETE MODAL */}
      <ConfirmModal
        isOpen={isDeleteModalOpen}
        title="Delete Document from Knowledge Base?"
        message={`Are you sure you want to delete "${docToDelete?.document_name}"? All associated semantic chunks and vectors will be removed from FAISS and BM25.`}
        confirmLabel="Delete Document"
        isDanger={true}
        loading={isDeleting}
        onConfirm={confirmDelete}
        onCancel={() => {
          setIsDeleteModalOpen(false);
          setDocToDelete(null);
        }}
      />
    </div>
  );
}
