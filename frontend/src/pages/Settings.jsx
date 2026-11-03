import { useState, useEffect } from "react";
import {
  Settings as SettingsIcon,
  Server,
  Activity,
  Sliders,
  Database,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Save,
  RotateCcw,
} from "lucide-react";
import {
  getApiBaseUrl,
  setApiBaseUrl,
  checkHealth,
  getKnowledgeBase,
  getSavedReports,
  clearSavedReports,
  clearSavedChat,
} from "../services/api";
import ConfirmModal from "../components/ui/ConfirmModal";

export default function Settings() {
  const [apiUrl, setApiUrl] = useState(getApiBaseUrl());
  const [healthStatus, setHealthStatus] = useState(null);
  const [testingHealth, setTestingHealth] = useState(false);
  const [docCount, setDocCount] = useState(0);
  const [reportsCount, setReportsCount] = useState(0);
  const [topK, setTopK] = useState(5);
  const [message, setMessage] = useState(null);

  const [isClearReportsOpen, setIsClearReportsOpen] = useState(false);
  const [isClearChatOpen, setIsClearChatOpen] = useState(false);

  useEffect(() => {
    loadInfo();
  }, []);

  const loadInfo = async () => {
    try {
      const kb = await getKnowledgeBase().catch(() => null);
      if (kb && kb.total_documents !== undefined) {
        setDocCount(kb.total_documents);
      }
      const saved = getSavedReports();
      setReportsCount(saved.length);
    } catch (err) {
      console.error(err);
    }
  };

  const handleTestConnection = async () => {
    setTestingHealth(true);
    setMessage(null);
    try {
      const res = await checkHealth();
      if (res?.status === "healthy") {
        setHealthStatus("healthy");
        setMessage({ type: "success", text: "Successfully connected to FastAPI backend!" });
      } else {
        setHealthStatus("offline");
        setMessage({ type: "warning", text: "Backend unreachable at this URL." });
      }
    } catch (err) {
      setHealthStatus("offline");
      setMessage({ type: "danger", text: err.message || "Connection failed." });
    } finally {
      setTestingHealth(false);
    }
  };

  const handleSaveApiUrl = () => {
    setApiBaseUrl(apiUrl);
    setMessage({ type: "success", text: "Backend URL updated successfully." });
    handleTestConnection();
  };

  const handleResetApiUrl = () => {
    localStorage.removeItem("aiba_api_url");
    const defaultUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
    setApiUrl(defaultUrl);
    setMessage({ type: "success", text: "Reset to default endpoint." });
  };

  const handleConfirmClearReports = () => {
    clearSavedReports();
    setReportsCount(0);
    setIsClearReportsOpen(false);
    setMessage({ type: "success", text: "Saved reports cleared." });
  };

  const handleConfirmClearChat = () => {
    clearSavedChat();
    setIsClearChatOpen(false);
    setMessage({ type: "success", text: "Chat history cleared." });
  };

  return (
    <div style={{ maxWidth: "860px", margin: "0 auto" }}>
      {/* HEADER */}
      <div style={{ marginBottom: "28px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "800", color: "#0f172a" }}>
          Workspace Settings & Diagnostics
        </h2>
        <p style={{ color: "#64748b", fontSize: "14px", marginTop: "4px" }}>
          Configure API connectivity, retrieval preferences, and local storage caches.
        </p>
      </div>

      {/* STATUS ALERT */}
      {message && (
        <div
          style={{
            padding: "12px 18px",
            borderRadius: "10px",
            marginBottom: "20px",
            fontSize: "13.5px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background:
              message.type === "success"
                ? "#ecfdf5"
                : message.type === "warning"
                ? "#fffbeb"
                : "#fef2f2",
            color:
              message.type === "success"
                ? "#065f46"
                : message.type === "warning"
                ? "#92400e"
                : "#991b1b",
            border: `1px solid ${
              message.type === "success"
                ? "#a7f3d0"
                : message.type === "warning"
                ? "#fde68a"
                : "#fecaca"
            }`,
          }}
        >
          {message.type === "success" ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
          <span>{message.text}</span>
        </div>
      )}

      {/* BACKEND CONFIGURATION */}
      <div className="card" style={{ padding: "24px", marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
          <div style={{ width: "34px", height: "34px", borderRadius: "8px", background: "#eff6ff", color: "#2563eb", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Server size={18} />
          </div>
          <div>
            <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>
              Backend API Endpoint
            </h3>
            <span style={{ fontSize: "12.5px", color: "#64748b" }}>
              The URL of your running FastAPI server
            </span>
          </div>
        </div>

        <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            placeholder="http://127.0.0.1:8000"
            style={{
              flex: 1,
              padding: "10px 14px",
              borderRadius: "8px",
              border: "1px solid #cbd5e1",
              fontSize: "14px",
              fontFamily: "var(--font-mono)",
            }}
          />
          <button onClick={handleSaveApiUrl} className="btn btn-primary btn-sm">
            <Save size={14} />
            <span>Save URL</span>
          </button>
          <button onClick={handleResetApiUrl} className="btn btn-secondary btn-sm" title="Reset to default">
            <RotateCcw size={14} />
          </button>
        </div>

        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: "12px", borderTop: "1px solid #f1f5f9" }}>
          <span style={{ fontSize: "12.5px", color: "#64748b" }}>
            Default: <code>http://127.0.0.1:8000</code>
          </span>
          <button
            onClick={handleTestConnection}
            className="btn btn-secondary btn-sm"
            disabled={testingHealth}
          >
            <Activity size={14} />
            <span>{testingHealth ? "Pinging..." : "Test Connection"}</span>
          </button>
        </div>
      </div>

      {/* RETRIEVAL SETTINGS */}
      <div className="card" style={{ padding: "24px", marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
          <div style={{ width: "34px", height: "34px", borderRadius: "8px", background: "#f5f3ff", color: "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Sliders size={18} />
          </div>
          <div>
            <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>
              Retrieval & RAG Parameters
            </h3>
            <span style={{ fontSize: "12.5px", color: "#64748b" }}>
              Control candidate depth for hybrid search & reranking
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 0" }}>
          <div>
            <strong style={{ fontSize: "14px", color: "#0f172a", display: "block" }}>
              Default Top-K Retrieved Chunks: {topK}
            </strong>
            <span style={{ fontSize: "12.5px", color: "#64748b" }}>
              Number of top cross-encoder reranked evidence items passed to the LLM.
            </span>
          </div>

          <div style={{ display: "flex", gap: "6px" }}>
            {[3, 5, 8, 10].map((k) => (
              <button
                key={k}
                onClick={() => setTopK(k)}
                style={{
                  padding: "6px 12px",
                  borderRadius: "6px",
                  border: "1px solid",
                  borderColor: topK === k ? "#2563eb" : "#cbd5e1",
                  background: topK === k ? "#eff6ff" : "#fff",
                  color: topK === k ? "#2563eb" : "#475569",
                  fontWeight: "600",
                  fontSize: "12px",
                  cursor: "pointer",
                }}
              >
                {k} chunks
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* STORAGE & DATA MANAGEMENT */}
      <div className="card" style={{ padding: "24px", marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
          <div style={{ width: "34px", height: "34px", borderRadius: "8px", background: "#fee2e2", color: "#dc2626", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Database size={18} />
          </div>
          <div>
            <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#0f172a" }}>
              Browser Data & Cache Management
            </h3>
            <span style={{ fontSize: "12.5px", color: "#64748b" }}>
              Manage local browser storage caches and saved analyses
            </span>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 0", borderBottom: "1px solid #f1f5f9" }}>
            <div>
              <strong style={{ fontSize: "13.5px", color: "#0f172a", display: "block" }}>
                Executive Reports ({reportsCount} saved)
              </strong>
              <span style={{ fontSize: "12px", color: "#64748b" }}>
                Locally saved dossiers from the Business Analysis studio.
              </span>
            </div>
            <button
              onClick={() => setIsClearReportsOpen(true)}
              className="btn btn-secondary btn-sm"
              disabled={reportsCount === 0}
              style={{ color: "#ef4444" }}
            >
              <Trash2 size={13} />
              <span>Clear Reports</span>
            </button>
          </div>

          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 0" }}>
            <div>
              <strong style={{ fontSize: "13.5px", color: "#0f172a", display: "block" }}>
                Chat History
              </strong>
              <span style={{ fontSize: "12px", color: "#64748b" }}>
                Locally saved multi-turn dialogue from the AI Chat.
              </span>
            </div>
            <button
              onClick={() => setIsClearChatOpen(true)}
              className="btn btn-secondary btn-sm"
              style={{ color: "#ef4444" }}
            >
              <Trash2 size={13} />
              <span>Clear Chat</span>
            </button>
          </div>
        </div>
      </div>

      {/* ABOUT PLATFORM */}
      <div className="card" style={{ padding: "24px", background: "#f8fafc" }}>
        <h4 style={{ fontSize: "14px", fontWeight: "700", color: "#0f172a", marginBottom: "8px" }}>
          AIBA · AI Business Analyst Platform
        </h4>
        <p style={{ fontSize: "13px", color: "#64748b", lineHeight: "1.6" }}>
          Version 2.0.0 · Open-access Architecture · Document Intelligence Engine
          <br />
          Built with React 19, Vite, FastAPI, Docling, FAISS, BM25, and Cross-Encoder Reranking.
        </p>
      </div>

      {/* CONFIRM MODALS */}
      <ConfirmModal
        isOpen={isClearReportsOpen}
        title="Clear all saved reports?"
        message="This will permanently delete all saved analysis dossiers from your browser's local cache."
        confirmLabel="Clear Reports"
        isDanger={true}
        onConfirm={handleConfirmClearReports}
        onCancel={() => setIsClearReportsOpen(false)}
      />

      <ConfirmModal
        isOpen={isClearChatOpen}
        title="Clear chat conversation history?"
        message="This will reset the conversation thread and wipe stored messages from this browser."
        confirmLabel="Clear Chat"
        isDanger={true}
        onConfirm={handleConfirmClearChat}
        onCancel={() => setIsClearChatOpen(false)}
      />
    </div>
  );
}
