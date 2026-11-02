import { useCallback, useEffect, useRef, useState } from "react";
import {
  getKnowledgeBase,
  uploadDocument,
  deleteDocument,
} from "../services/api";
import "./knowledge-base.css";

function formatDate(dateString) {
  if (!dateString) return "—";

  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) return dateString;

  return date.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function KnowledgeBase() {
  const [documents, setDocuments] = useState([]);
  const [totalDocuments, setTotalDocuments] = useState(0);

  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fileInputRef = useRef(null);

  const loadDocuments = useCallback(async () => {
    try {
      setError("");

      const data = await getKnowledgeBase();

      setDocuments(data.documents || []);
      setTotalDocuments(data.total_documents ?? 0);
    } catch (err) {
      setError(err.message || "Unable to load the Knowledge Base.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];

    // Allow selecting the same file again later.
    event.target.value = "";

    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      setSuccess("");
      return;
    }

    try {
      setUploading(true);
      setError("");
      setSuccess("");

      const result = await uploadDocument(file);

      setSuccess(
        `${result.message} ${result.pages} pages and ${result.chunks_created} chunks processed.`
      );

      await loadDocuments();
    } catch (err) {
      setError(err.message || "Document upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (document) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${document.document_name}" from your Knowledge Base?`
    );

    if (!confirmed) return;

    try {
      setDeletingId(document.document_id);
      setError("");
      setSuccess("");

      await deleteDocument(document.document_id);

      setSuccess(`"${document.document_name}" was deleted successfully.`);

      await loadDocuments();
    } catch (err) {
      setError(err.message || "Unable to delete this document.");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <section className="kb-page">
      <div className="kb-heading">
        <div>
          <h2>Your Knowledge Base</h2>
          <p>
            Upload and manage the documents that power your AI business
            intelligence.
          </p>
        </div>

        <button
          className="kb-upload-button"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "+ Upload PDF"}
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          hidden
          onChange={handleUpload}
        />
      </div>

      <div className="kb-stats">
        <div className="kb-stat-card">
          <span className="kb-stat-label">Total Documents</span>
          <strong>{totalDocuments}</strong>
          <span className="kb-stat-description">
            Documents stored in your workspace
          </span>
        </div>
      </div>

      {success && (
        <div className="kb-alert kb-alert-success" role="status">
          {success}
        </div>
      )}

      {error && (
        <div className="kb-alert kb-alert-error" role="alert">
          {error}
        </div>
      )}

      <div className="kb-document-section">
        <div className="kb-section-heading">
          <div>
            <h3>Uploaded Documents</h3>
            <p>Manage the files available to your AI assistant.</p>
          </div>

          <button
            className="kb-refresh-button"
            onClick={loadDocuments}
            disabled={loading || uploading}
          >
            ↻ Refresh
          </button>
        </div>

        {loading ? (
          <div className="kb-state">
            <div className="kb-spinner" />
            <p>Loading your documents...</p>
          </div>
        ) : documents.length === 0 ? (
          <div className="kb-empty-state">
            <div className="kb-empty-icon">📄</div>
            <h3>Your Knowledge Base is empty</h3>
            <p>
              Upload your first PDF to start asking questions and generating
              business insights from your documents.
            </p>
            <button
              className="kb-upload-button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
            >
              Upload your first document
            </button>
          </div>
        ) : (
          <div className="kb-table-wrapper">
            <table className="kb-table">
              <thead>
                <tr>
                  <th>Document</th>
                  <th>File Type</th>
                  <th>Pages</th>
                  <th>Uploaded</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {documents.map((document) => (
                  <tr key={document.document_id}>
                    <td>
                      <div className="kb-document-name">
                        <span className="kb-pdf-icon">PDF</span>
                        <div>
                          <strong>{document.document_name}</strong>
                          {document.title && (
                            <span>{document.title}</span>
                          )}
                        </div>
                      </div>
                    </td>

                    <td>{document.file_type || "PDF"}</td>

                    <td>{document.total_pages ?? 0}</td>

                    <td>{formatDate(document.created_at)}</td>

                    <td>
                      <button
                        className="kb-delete-button"
                        onClick={() => handleDelete(document)}
                        disabled={deletingId === document.document_id}
                      >
                        {deletingId === document.document_id
                          ? "Deleting..."
                          : "Delete"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export default KnowledgeBase;