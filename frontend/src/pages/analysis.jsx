import { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import {
  BarChart3,
  Sparkles,
  Send,
  GitCompare,
  ShieldCheck,
  TrendingUp,
  AlertCircle,
  PieChart,
  Copy,
  Check,
  Download,
  Bookmark,
  CheckCircle2,
  FileText,
  Layers,
  ChevronDown,
} from "lucide-react";
import { analyzeBusiness, saveReport } from "../services/api";
import "./analysis.css";

const analysisTemplates = [
  {
    id: "comparative",
    name: "Comparative Analysis",
    icon: GitCompare,
    prompt:
      "Compare the revenue, operating margins, and growth trajectory of the different business units or operating segments.",
  },
  {
    id: "swot",
    name: "SWOT Assessment",
    icon: ShieldCheck,
    prompt:
      "Provide an evidence-grounded SWOT analysis identifying key internal strengths, operational weaknesses, market opportunities, and competitive threats.",
  },
  {
    id: "trend",
    name: "Trend & Trajectory",
    icon: TrendingUp,
    prompt:
      "Analyze historical trends and multi-period changes across revenue, gross margins, and capital expenditures.",
  },
  {
    id: "rootcause",
    name: "Root Cause Diagnostics",
    icon: AlertCircle,
    prompt:
      "Identify the primary operational or macroeconomic root causes behind any margin compression, supply delays, or cost overruns.",
  },
  {
    id: "contribution",
    name: "Contribution Model",
    icon: PieChart,
    prompt:
      "Analyze how individual product lines, customer segments, or geographic regions contribute to total enterprise profit.",
  },
];

export default function Analysis() {
  const location = useLocation();

  const [query, setQuery] = useState("");
  const [activeTemplate, setActiveTemplate] = useState("comparative");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (location.state?.prefilledQuery) {
      setQuery(location.state.prefilledQuery);
    }
  }, [location.state]);

  const handleSelectTemplate = (tmpl) => {
    setActiveTemplate(tmpl.id);
    setQuery(tmpl.prompt);
  };

  const handleAnalysis = async (e) => {
    if (e) e.preventDefault();
    const q = query.trim();
    if (!q || loading) return;

    try {
      setLoading(true);
      setError("");
      setResult(null);
      setSavedSuccess(false);

      const data = await analyzeBusiness(q);
      setResult(data);

      // Auto-save to local reports archive
      saveReport({
        query: q,
        analysis_type: data.analysis_type || "Business Analysis",
        findings: data.findings || [],
        conclusions: data.conclusions || [],
        supporting_evidence: data.supporting_evidence || [],
      });
      setSavedSuccess(true);
    } catch (err) {
      setError(
        err.message ||
          "Unable to generate analysis. Verify your backend is running at http://127.0.0.1:8000."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleCopyAnalysis = () => {
    if (!result) return;
    let text = `# AIBA Business Analysis: ${result.analysis_type || "Generated Insights"}\n\n`;
    text += `**Query:** ${query}\n\n`;

    if (result.findings?.length) {
      text += `## Key Findings\n`;
      result.findings.forEach((f) => {
        text += `- ${f}\n`;
      });
      text += `\n`;
    }

    if (result.conclusions?.length) {
      text += `## Conclusions\n`;
      result.conclusions.forEach((c) => {
        text += `- ${c}\n`;
      });
      text += `\n`;
    }

    if (result.supporting_evidence?.length) {
      text += `## Supporting Evidence\n`;
      result.supporting_evidence.forEach((ev, i) => {
        text += `[${i + 1}] ${ev}\n\n`;
      });
    }

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadReport = () => {
    if (!result) return;
    let text = `# AIBA Business Analysis Report\n\n`;
    text += `**Date:** ${new Date().toLocaleString()}\n`;
    text += `**Analysis Type:** ${result.analysis_type}\n`;
    text += `**Query:** ${query}\n\n---\n\n`;

    if (result.findings?.length) {
      text += `## Key Findings\n\n`;
      result.findings.forEach((f) => {
        text += `- ${f}\n`;
      });
      text += `\n`;
    }

    if (result.conclusions?.length) {
      text += `## Strategic Conclusions\n\n`;
      result.conclusions.forEach((c) => {
        text += `- ${c}\n`;
      });
      text += `\n`;
    }

    if (result.supporting_evidence?.length) {
      text += `## Supporting Citations\n\n`;
      result.supporting_evidence.forEach((ev, i) => {
        text += `### Citation [${i + 1}]\n${ev}\n\n`;
      });
    }

    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AIBA_Analysis_${(result.analysis_type || "Analysis").replace(/\s+/g, "_")}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="analysis-studio">
      {/* HEADER */}
      <div className="analysis-hero-bar">
        <div>
          <h2>Business Analysis Studio</h2>
          <p>
            Structured strategic reasoning: evaluate segment margins, SWOT matrices, and multi-period trends.
          </p>
        </div>

        <Link to="/reports" className="btn btn-secondary btn-sm">
          <FileText size={14} />
          <span>View Saved Reports</span>
        </Link>
      </div>

      {/* INPUT CARD */}
      <div className="analysis-input-card">
        <label
          style={{
            display: "block",
            fontSize: "12px",
            fontWeight: "700",
            color: "#64748b",
            textTransform: "uppercase",
            marginBottom: "10px",
          }}
        >
          Select Analytical Framework
        </label>

        <div className="frameworks-selector">
          {analysisTemplates.map((t) => {
            const Icon = t.icon;
            return (
              <button
                key={t.id}
                type="button"
                className={`framework-btn ${activeTemplate === t.id ? "active" : ""}`}
                onClick={() => handleSelectTemplate(t)}
              >
                <Icon size={14} />
                <span>{t.name}</span>
              </button>
            );
          })}
        </div>

        <form onSubmit={handleAnalysis}>
          <textarea
            className="analysis-textarea"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your strategic inquiry or select a framework above..."
            rows={4}
            disabled={loading}
          />

          <div className="analysis-form-footer">
            <span style={{ fontSize: "12.5px", color: "#64748b" }}>
              AIBA will evaluate question type, retrieve evidence, and synthesize findings.
            </span>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !query.trim()}
              style={{ padding: "10px 22px" }}
            >
              {loading ? (
                <>
                  <Sparkles size={16} className="animate-spin" />
                  <span>Synthesizing...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>Execute Analysis</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div
          style={{
            padding: "16px 20px",
            borderRadius: "12px",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            color: "#991b1b",
            fontSize: "13.5px",
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >
          <AlertCircle size={20} style={{ flexShrink: 0 }} />
          <div>
            <strong>Analysis Failed:</strong> {error}
          </div>
        </div>
      )}

      {/* LOADING STATE */}
      {loading && (
        <div
          className="card"
          style={{
            padding: "48px 24px",
            textAlign: "center",
            background: "#ffffff",
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              border: "3px solid #eff6ff",
              borderTopColor: "#2563eb",
              animation: "spin 1s linear infinite",
              margin: "0 auto 16px",
            }}
          />
          <h3 style={{ fontSize: "18px", fontWeight: "700", color: "#0f172a" }}>
            Analyzing Document Repository...
          </h3>
          <p style={{ color: "#64748b", fontSize: "13.5px", maxWidth: "460px", margin: "6px auto 0" }}>
            Executing hybrid vector + BM25 search, applying cross-encoder reranking, and evaluating business conclusions.
          </p>
        </div>
      )}

      {/* EMPTY STATE */}
      {!loading && !result && !error && (
        <div
          className="card"
          style={{
            padding: "50px 20px",
            textAlign: "center",
            background: "#ffffff",
            border: "1px dashed #cbd5e1",
          }}
        >
          <div
            style={{
              width: "52px",
              height: "52px",
              borderRadius: "14px",
              background: "#eff6ff",
              color: "#2563eb",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px",
            }}
          >
            <BarChart3 size={26} />
          </div>
          <h3 style={{ fontSize: "18px", fontWeight: "700", color: "#0f172a" }}>
            Ready for Business Intelligence Interrogation
          </h3>
          <p style={{ color: "#64748b", fontSize: "14px", maxWidth: "480px", margin: "8px auto 0", lineHeight: "1.5" }}>
            Select one of the strategic frameworks above or formulate a custom business inquiry to extract grounded findings.
          </p>
        </div>
      )}

      {/* ANALYSIS RESULT */}
      {result && (
        <div className="analysis-output-container">
          {/* Header Bar */}
          <div className="analysis-header-card">
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
                <span
                  className="badge"
                  style={{
                    background: "#eff6ff",
                    color: "#2563eb",
                    border: "1px solid #bfdbfe",
                    fontSize: "12px",
                  }}
                >
                  {result.analysis_type || "Business Analysis"}
                </span>
                {savedSuccess && (
                  <span style={{ fontSize: "12px", color: "#059669", display: "flex", alignItems: "center", gap: "4px", fontWeight: "600" }}>
                    <CheckCircle2 size={13} />
                    <span>Saved to Reports Archive</span>
                  </span>
                )}
              </div>
              <h3 style={{ fontSize: "17px", fontWeight: "700", color: "#0f172a" }}>
                Executive Intelligence Brief
              </h3>
            </div>

            <div style={{ display: "flex", gap: "8px" }}>
              <button
                onClick={handleCopyAnalysis}
                className="btn btn-secondary btn-sm"
              >
                {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                <span>{copied ? "Copied" : "Copy Brief"}</span>
              </button>

              <button
                onClick={handleDownloadReport}
                className="btn btn-primary btn-sm"
              >
                <Download size={14} />
                <span>Export Markdown</span>
              </button>
            </div>
          </div>

          {/* Key Findings */}
          <div className="card" style={{ padding: "24px" }}>
            <h4
              style={{
                fontSize: "13px",
                fontWeight: "700",
                color: "#2563eb",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                marginBottom: "16px",
              }}
            >
              Key Analytical Findings ({result.findings?.length || 0})
            </h4>

            {result.findings?.length ? (
              <div className="findings-grid">
                {result.findings.map((finding, idx) => (
                  <div key={idx} className="finding-card">
                    <span className="finding-number">{idx + 1}</span>
                    <span className="finding-text">{finding}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: "#94a3b8", fontSize: "13.5px" }}>No findings generated.</p>
            )}
          </div>

          {/* Conclusions */}
          <div className="conclusions-section">
            <h4
              style={{
                fontSize: "13px",
                fontWeight: "700",
                color: "#166534",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                marginBottom: "8px",
              }}
            >
              Strategic Conclusions & Takeaways
            </h4>

            {result.conclusions?.length ? (
              <ul className="conclusions-list">
                {result.conclusions.map((conclusion, idx) => (
                  <li key={idx}>{conclusion}</li>
                ))}
              </ul>
            ) : (
              <p style={{ color: "#166534", fontSize: "13.5px" }}>No conclusions generated.</p>
            )}
          </div>

          {/* Supporting Evidence */}
          <div className="evidence-box">
            <h4
              style={{
                fontSize: "13px",
                fontWeight: "700",
                color: "#64748b",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                marginBottom: "12px",
              }}
            >
              Supporting Document Citations ({result.supporting_evidence?.length || 0})
            </h4>

            {result.supporting_evidence?.length ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                {result.supporting_evidence.map((evidence, idx) => (
                  <div key={idx} className="evidence-item-card">
                    <strong style={{ display: "block", color: "#0f172a", marginBottom: "4px" }}>
                      Evidence Citation [{idx + 1}]
                    </strong>
                    <p style={{ margin: 0 }}>{evidence}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: "#94a3b8", fontSize: "13.5px" }}>No supporting citations provided.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
