import { useRef, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import {
  Sparkles,
  Send,
  Trash2,
  Copy,
  Check,
  ChevronDown,
  Download,
  AlertCircle,
  Clock,
  Layers,
  FileCheck,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { sendChatMessage, getSavedChat, saveChat, clearSavedChat } from "../services/api";
import ConfirmModal from "../components/ui/ConfirmModal";
import "./chat.css";

const starterPrompts = [
  {
    category: "Financials",
    title: "Operating Margins",
    query: "Compare operating margins and EBITDA trajectory across reported business units.",
    icon: TrendingUp,
  },
  {
    category: "Risk Audit",
    title: "Key Business Risks",
    query: "Identify and synthesize the primary operational, legal, and liquidity risks cited in the documents.",
    icon: ShieldCheck,
  },
  {
    category: "Operations",
    title: "Supply Chain Bottlenecks",
    query: "What specific supply chain, inventory, or procurement constraints are highlighted?",
    icon: Layers,
  },
  {
    category: "Strategic",
    title: "Executive Summary",
    query: "Provide an executive summary of high-level performance drivers and future strategic guidance.",
    icon: FileCheck,
  },
];

export default function Chat() {
  const location = useLocation();
  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState(() => getSavedChat());
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copiedId, setCopiedId] = useState(null);
  const [isConfirmClearOpen, setIsConfirmClearOpen] = useState(false);

  // Check if routed with a prefilled query
  useEffect(() => {
    if (location.state?.prefilledQuery) {
      setQuery(location.state.prefilledQuery);
      inputRef.current?.focus();
    }
  }, [location.state]);

  // Persist messages whenever updated
  useEffect(() => {
    saveChat(messages);
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (event) => {
    if (event) event.preventDefault();
    const question = query.trim();
    if (!question || loading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setError("");
    setLoading(true);

    try {
      const result = await sendChatMessage(question, 5);

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: result.answer || "No response received.",
        retrievalResults: result.retrieval_results || [],
        llm: result.llm,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(
        err.message ||
          "Unable to generate response. Ensure the backend server is running (uvicorn app.main:app --reload)."
      );
    } finally {
      setLoading(false);
      setTimeout(scrollToBottom, 100);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleExportChat = () => {
    if (messages.length === 0) return;
    let md = `# AIBA Assistant Chat Transcript\n\n`;
    md += `*Exported on ${new Date().toLocaleString()}*\n\n---\n\n`;

    messages.forEach((m) => {
      md += `### ${m.role === "user" ? "User" : "AIBA Assistant"} (${new Date(m.timestamp).toLocaleTimeString()})\n\n`;
      md += `${m.content}\n\n`;
      if (m.retrievalResults && m.retrievalResults.length > 0) {
        md += `*Supporting Evidence (${m.retrievalResults.length} chunks retrieved)*\n\n`;
      }
      md += `---\n\n`;
    });

    const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AIBA_Chat_${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const confirmClear = () => {
    setMessages([]);
    clearSavedChat();
    setError("");
    setIsConfirmClearOpen(false);
  };

  return (
    <section className="chat-page">
      {/* TOOLBAR */}
      <div className="chat-toolbar">
        <div>
          <h2>AI Business Assistant</h2>
          <p>
            Natural-language dialogue grounded in your Knowledge Base with cross-encoder evidence attribution.
          </p>
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          {messages.length > 0 && (
            <>
              <button
                onClick={handleExportChat}
                className="btn btn-secondary btn-sm"
                title="Download chat as Markdown"
              >
                <Download size={13} />
                <span>Export Chat</span>
              </button>

              <button
                onClick={() => setIsConfirmClearOpen(true)}
                className="btn btn-secondary btn-sm"
                style={{ color: "#ef4444" }}
                disabled={loading}
              >
                <Trash2 size={13} />
                <span>Clear Thread</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* CHAT CONTAINER */}
      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <div className="chat-welcome-icon">
                <Sparkles size={28} />
              </div>

              <h2>How can I assist your business analysis today?</h2>
              <p>
                Ask detailed financial, operational, or strategic questions about your indexed documents.
                AIBA retrieves relevant passages, reranks them for precision, and cites evidence.
              </p>

              <div className="chat-suggestions-grid">
                {starterPrompts.map((item, idx) => {
                  const Icon = item.icon;
                  return (
                    <div
                      key={idx}
                      className="suggestion-chip"
                      onClick={() => {
                        setQuery(item.query);
                        inputRef.current?.focus();
                      }}
                    >
                      <strong>
                        <Icon size={14} color="#2563eb" />
                        <span>{item.title}</span>
                      </strong>
                      <span>"{item.query}"</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-message-row ${message.role}`}
            >
              <div className={`chat-avatar-badge ${message.role}`}>
                {message.role === "user" ? "You" : <Sparkles size={16} />}
              </div>

              <div className="chat-bubble">
                <div className="message-header">
                  <strong>
                    {message.role === "user" ? "You" : "AIBA Analyst"}
                  </strong>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span className="time">
                      {new Date(message.timestamp || Date.now()).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                    <button
                      onClick={() => handleCopy(message.id, message.content)}
                      style={{
                        background: "none",
                        border: "none",
                        cursor: "pointer",
                        color: message.role === "user" ? "#94a3b8" : "#64748b",
                        padding: "2px",
                      }}
                      title="Copy message"
                    >
                      {copiedId === message.id ? (
                        <Check size={13} color="#10b981" />
                      ) : (
                        <Copy size={13} />
                      )}
                    </button>
                  </div>
                </div>

                <div className="message-text">{message.content}</div>

                {message.role === "assistant" && (
                  <>
                    {/* Supporting Evidence Drawer */}
                    {message.retrievalResults?.length > 0 && (
                      <details className="chat-evidence-details">
                        <summary className="chat-evidence-summary">
                          <span>
                            Supporting Evidence ({message.retrievalResults.length} chunks retrieved)
                          </span>
                        </summary>

                        <div className="chat-evidence-list">
                          {message.retrievalResults.map((item, idx) => (
                            <div className="chat-evidence-card" key={item.chunk_id || idx}>
                              <div className="evidence-meta-row">
                                <span className="evidence-title">
                                  {item.title || "Indexed Document Chunk"}
                                </span>

                                <span className="evidence-score-badge">
                                  {item.rerank_score != null
                                    ? `Rerank: ${item.rerank_score.toFixed(3)}`
                                    : item.retrieval_score != null
                                    ? `Score: ${item.retrieval_score.toFixed(3)}`
                                    : "Retrieved"}
                                </span>
                              </div>

                              <p className="evidence-text">{item.text}</p>
                            </div>
                          ))}
                        </div>
                      </details>
                    )}

                    {/* LLM Usage Strip */}
                    {message.llm && (
                      <div className="chat-usage-strip">
                        <span>Tokens: In: {message.llm.input_tokens ?? "—"}</span>
                        <span>·</span>
                        <span>Out: {message.llm.output_tokens ?? "—"}</span>
                        <span>·</span>
                        <span>Total: {message.llm.total_tokens ?? "—"}</span>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-message-row assistant">
              <div className="chat-avatar-badge assistant">
                <Sparkles size={16} />
              </div>
              <div className="chat-bubble">
                <div className="message-header">
                  <strong>AIBA Analyst</strong>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", color: "#64748b" }}>
                  <div className="typing-dots">
                    <span />
                    <span />
                    <span />
                  </div>
                  <span style={{ fontSize: "13px" }}>
                    Executing hybrid search, reranking chunks, and synthesizing response...
                  </span>
                </div>
              </div>
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
              role="alert"
            >
              <AlertCircle size={18} style={{ flexShrink: 0 }} />
              <div>
                <strong>Query Error:</strong> {error}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* INPUT BAR */}
        <form className="chat-input-bar" onSubmit={handleSubmit}>
          <div className="input-row">
            <textarea
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask an analytical question about your business filings..."
              className="chat-textarea"
              rows={2}
              disabled={loading}
            />

            <button
              type="submit"
              className="btn btn-primary"
              style={{ height: "48px", padding: "0 20px" }}
              disabled={!query.trim() || loading}
            >
              {loading ? (
                <span>Thinking...</span>
              ) : (
                <>
                  <span>Send</span>
                  <Send size={15} />
                </>
              )}
            </button>
          </div>

          <div className="input-hint-row">
            <span>Press Enter to send · Shift + Enter for new line</span>
            <span>Hybrid Search: FAISS + BM25 + Cross-Encoder</span>
          </div>
        </form>
      </div>

      <ConfirmModal
        isOpen={isConfirmClearOpen}
        title="Clear conversation thread?"
        message="This will wipe all active messages in this dialogue from your browser storage."
        confirmLabel="Clear Thread"
        isDanger={true}
        onConfirm={confirmClear}
        onCancel={() => setIsConfirmClearOpen(false)}
      />
    </section>
  );
}
