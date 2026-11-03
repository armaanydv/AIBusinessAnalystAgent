import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Sparkles,
  ArrowRight,
  Database,
  Search,
  Cpu,
  BarChart3,
  FileCheck,
  ShieldCheck,
  Zap,
  ChevronDown,
  Layers,
  CheckCircle2,
  ExternalLink,
  LineChart,
  GitCompare,
  TrendingUp,
  AlertCircle,
  FileText,
} from "lucide-react";
import { checkHealth, getKnowledgeBase } from "../services/api";
import "./landing.css";

const analysisCapabilities = [
  {
    id: "comparative",
    title: "Comparative Analysis",
    icon: GitCompare,
    subtitle: "Cross-segment & cross-period benchmarking",
    description:
      "Benchmark business units, quarterly revenue streams, operational expenses, and product divisions against one another with verifiable evidence.",
    sampleQuery:
      "Compare Q3 vs Q4 operating margin performance across Cloud and Enterprise divisions and identify the primary cost inflation drivers.",
    findings: [
      "Enterprise division margins expanded by 240 bps to 28.4% due to reduced customer acquisition expenditures.",
      "Cloud segment experienced 180 bps compression driven by data center infrastructure and GPU cluster leasing commitments.",
      "Consolidated operating leverage remained net positive at 14.2% YoY growth.",
    ],
    conclusions: [
      "Capital reallocation toward automated cloud provisioning is recommended to recover segment gross margins by Q2.",
      "Enterprise software retention rates (96.4%) buffer macroeconomic softness.",
    ],
    evidence: "Doc: FY24_Financial_Report.pdf (Page 42, Chunk #108) — Rerank Score: 0.942",
  },
  {
    id: "swot",
    title: "SWOT Analysis",
    icon: ShieldCheck,
    subtitle: "Strategic enterprise posture assessment",
    description:
      "Synthesize thousands of pages into crisp, audit-grade Strengths, Weaknesses, Opportunities, and Threats grounded entirely in indexed filings.",
    sampleQuery:
      "Generate an evidence-backed SWOT analysis for our expansion into European manufacturing hubs.",
    findings: [
      "Strength: Existing EU regulatory clearance and established supply chain partnerships in Germany.",
      "Weakness: Higher energy tariffs and mandatory collective bargaining agreements raising unit cost by 8.5%.",
      "Opportunity: Regional EU green subsidies offsetting up to €14M in facility retrofitting costs.",
      "Threat: Currency volatility between EUR/USD and impending cross-border carbon border adjustment mechanisms.",
    ],
    conclusions: [
      "Prioritize green-energy procurement contracts in Q1 to qualify for tax offset credits.",
    ],
    evidence: "Doc: Global_Expansion_Strategy_2025.pdf (Page 18, Chunk #047) — Rerank Score: 0.915",
  },
  {
    id: "trend",
    title: "Trend & Trajectory",
    icon: TrendingUp,
    subtitle: "Multi-quarter momentum & trajectory detection",
    description:
      "Identify subtle margin contractions, seasonal revenue cyclicality, and operational velocity shifts over successive fiscal periods.",
    sampleQuery:
      "Analyze the 3-year trajectory of customer acquisition cost (CAC) versus customer lifetime value (LTV).",
    findings: [
      "CAC increased from $420 in FY22 to $685 in FY24, representing a 63% cost inflation over 24 months.",
      "LTV expansion stabilized at $3,400 due to extended multi-year enterprise contract renewals.",
      "LTV:CAC ratio contracted from 8.1x to 4.96x, still healthy but signaling paid channel saturation.",
    ],
    conclusions: [
      "Shift outbound marketing spend toward product-led expansion and existing account upsell motions.",
    ],
    evidence: "Doc: Annual_Investor_Presentation_2024.pdf (Page 64, Chunk #132) — Rerank Score: 0.898",
  },
  {
    id: "rootcause",
    title: "Root Cause Diagnostics",
    icon: AlertCircle,
    subtitle: "Isolate operational anomalies and drivers",
    description:
      "Dissect operational delays, inventory build-ups, and cash flow compression back to the exact contractual or logistical driver.",
    sampleQuery:
      "What were the primary root causes for the inventory write-downs in the consumer electronics sector during Q2?",
    findings: [
      "Component redesign lead time was delayed by 14 weeks due to single-source micro-controller allocations in East Asia.",
      "Over-forecasting of holiday consumer demand resulted in 34,000 obsolete SKU units held past product lifecycle cutoff.",
      "Warehouse holding fees escalated by 28% due to extended dwell times at third-party logistics ports.",
    ],
    conclusions: [
      "Dual-sourcing policy must be enforced for critical semiconductor bill-of-materials.",
    ],
    evidence: "Doc: Operations_Review_Q2.pdf (Page 11, Chunk #029) — Rerank Score: 0.931",
  },
];

const faqs = [
  {
    q: "How does AIBA prevent LLM hallucinations?",
    a: "AIBA employs a multi-tiered grounded RAG architecture. Document context is parsed with Docling to preserve table layouts and hierarchies, indexed with BGE embeddings in FAISS, retrieved in tandem with BM25 lexical keyword matching, and reranked using a deep cross-encoder. The prompt enforces strict citation against the retrieved chunks, ensuring that every finding references verifiable text.",
  },
  {
    q: "What types of business documents are supported?",
    a: "AIBA is optimized for complex business PDFs, including annual 10-K/10-Q reports, investor presentations, strategic market research decks, audited financial statements, board packs, and operational audit reports.",
  },
  {
    q: "What makes AIBA different from standard PDF chat wrappers?",
    a: "Standard chat wrappers blindly chunk text into arbitrary sizes and do basic vector search. AIBA builds structured document hierarchies, performs hybrid search with Reciprocal Rank Fusion (RRF), cross-encoder reordering, and executes pre-configured business analyst frameworks (SWOT, comparative, trend, and contribution analyses) that output executive-ready findings and conclusions.",
  },
  {
    q: "Is any user authentication required?",
    a: "AIBA is designed with an open-access philosophy. You can immediately upload PDFs and query the system without login barriers, credentials, or signup friction, making it ideal for fast collaborative workspaces and internal analyst benches.",
  },
  {
    q: "Can I export or save generated reports?",
    a: "Yes! AIBA features an Executive Reports workspace where your analyses are automatically preserved and can be viewed, copied, or exported into Markdown and JSON files for your executive presentations.",
  },
];

export default function LandingPage() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("comparative");
  const [openFaq, setOpenFaq] = useState(null);
  const [backendHealth, setBackendHealth] = useState(null);
  const [indexedDocCount, setIndexedDocCount] = useState(null);

  useEffect(() => {
    async function loadStatus() {
      try {
        const health = await checkHealth();
        setBackendHealth(health?.status === "healthy");
        const kb = await getKnowledgeBase();
        if (kb && kb.total_documents !== undefined) {
          setIndexedDocCount(kb.total_documents);
        }
      } catch {
        setBackendHealth(false);
      }
    }
    loadStatus();
  }, []);

  const currentCapability =
    analysisCapabilities.find((item) => item.id === activeTab) ||
    analysisCapabilities[0];

  const handleLaunchWithPrompt = (promptText) => {
    navigate("/analysis", { state: { prefilledQuery: promptText } });
  };

  return (
    <div className="landing-page">
      <div className="landing-glow-top" />
      <div className="landing-glow-mid" />

      {/* NAVBAR */}
      <header className="landing-nav">
        <div className="landing-container landing-nav-inner">
          <Link to="/" className="landing-brand">
            <div className="landing-brand-logo">
              <Sparkles size={22} color="#ffffff" />
            </div>
            <span className="landing-brand-name">AIBA</span>
            <span className="landing-brand-badge">Agent 2.0</span>
          </Link>

          <nav className="landing-nav-links">
            <a href="#features">Features</a>
            <a href="#capabilities">Capabilities</a>
            <a href="#architecture">Architecture</a>
            <a href="#faq">FAQ</a>
            <Link to="/methodology">Methodology</Link>
          </nav>

          <div className="landing-nav-cta">
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "12px",
                color: backendHealth ? "#34d399" : "#fbbf24",
                background: "rgba(255, 255, 255, 0.04)",
                padding: "6px 12px",
                borderRadius: "999px",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
              title={
                backendHealth
                  ? "FastAPI RAG Backend Online"
                  : "Local Backend Offline (Run: uvicorn app.main:app --reload)"
              }
            >
              <span
                style={{
                  width: "7px",
                  height: "7px",
                  borderRadius: "50%",
                  background: backendHealth ? "#10b981" : "#f59e0b",
                  boxShadow: backendHealth ? "0 0 8px #10b981" : "none",
                }}
              />
              <span>{backendHealth ? "API Connected" : "Local Engine"}</span>
            </div>

            <Link to="/dashboard" className="hero-btn-primary" style={{ padding: "9px 20px", fontSize: "13.5px" }}>
              <span>Launch Workspace</span>
              <ArrowRight size={15} />
            </Link>
          </div>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="landing-hero">
        <div className="landing-container">
          <div className="hero-pill">
            <span className="hero-pill-badge">Zero-Hallucination</span>
            <span>RAG Document Intelligence for Executive Decision Making</span>
          </div>

          <h1>
            Turn Complex Business Documents into{" "}
            <span className="gradient-text">Evidence-Backed Strategic Intelligence</span>
          </h1>

          <p className="hero-subtitle">
            AIBA combines Docling deep PDF parsing, semantic chunk hierarchies,
            FAISS vector search, BM25 keyword matching, cross-encoder reranking,
            and specialized business analyst reasoning to deliver audit-grade answers in seconds.
          </p>

          <div className="hero-actions">
            <Link to="/dashboard" className="hero-btn-primary">
              <Zap size={18} />
              <span>Launch AIBA Workspace</span>
              <ArrowRight size={16} />
            </Link>

            <Link to="/knowledge-base" className="hero-btn-secondary">
              <Database size={17} />
              <span>
                {indexedDocCount !== null && indexedDocCount > 0
                  ? `Knowledge Base (${indexedDocCount} Indexed)`
                  : "Upload & Explore Documents"}
              </span>
            </Link>

            <Link to="/methodology" className="hero-btn-secondary">
              <Cpu size={17} />
              <span>Inspect RAG Pipeline</span>
            </Link>
          </div>

          {/* TECH STRIP */}
          <div className="hero-tech-strip">
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>Docling PDF Parser</span>
            </div>
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>BGE Embeddings</span>
            </div>
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>FAISS Cosine Similarity</span>
            </div>
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>BM25 Keyword Engine</span>
            </div>
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>Reciprocal Rank Fusion</span>
            </div>
            <div className="hero-tech-item">
              <span className="hero-tech-dot" />
              <span>Cross-Encoder Reranker</span>
            </div>
          </div>

          {/* INTERACTIVE DEMO CARD */}
          <div className="hero-demo-wrapper">
            <div className="hero-demo-card">
              <div className="demo-card-header">
                <div className="window-dots">
                  <div className="window-dot red" />
                  <div className="window-dot yellow" />
                  <div className="window-dot green" />
                </div>
                <div className="demo-header-title">
                  <span>AIBA // RAG_PIPELINE_ORCHESTRATOR_V2</span>
                </div>
                <div className="demo-live-badge">
                  <CheckCircle2 size={12} />
                  <span>Verified Evidence</span>
                </div>
              </div>

              <div className="demo-card-body">
                {/* Left query and pipeline */}
                <div className="demo-query-box">
                  <div className="demo-box-label">
                    <Search size={12} />
                    <span>Business Query</span>
                  </div>
                  <p className="demo-query-text">
                    "Compare Q3 vs Q4 operating margins for the Cloud segment and isolate the primary cost drivers."
                  </p>

                  <div className="demo-pipeline-flow">
                    <div className="demo-step">
                      <span className="demo-step-name">
                        <Database size={13} color="#38bdf8" />
                        <span>FAISS Vector Retrieval (Top-15)</span>
                      </span>
                      <span className="demo-step-score">0.892 Cosine</span>
                    </div>

                    <div className="demo-step">
                      <span className="demo-step-name">
                        <Search size={13} color="#a78bfa" />
                        <span>BM25 Lexical Keyword Search</span>
                      </span>
                      <span className="demo-step-score">18.4 BM25</span>
                    </div>

                    <div className="demo-step">
                      <span className="demo-step-name">
                        <Layers size={13} color="#f472b6" />
                        <span>Reciprocal Rank Fusion (RRF)</span>
                      </span>
                      <span className="demo-step-score">Merged Top-5</span>
                    </div>

                    <div className="demo-step" style={{ border: "1px solid rgba(52, 211, 153, 0.3)" }}>
                      <span className="demo-step-name">
                        <Cpu size={13} color="#34d399" />
                        <span>Cross-Encoder Reranker</span>
                      </span>
                      <span className="demo-step-score" style={{ background: "rgba(16, 185, 129, 0.25)" }}>
                        0.942 Rerank
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right Output */}
                <div className="demo-output-box">
                  <div className="demo-box-label" style={{ color: "#34d399" }}>
                    <BarChart3 size={12} />
                    <span>Synthesized Findings</span>
                  </div>

                  <ul className="demo-findings-list">
                    <li className="demo-finding-item">
                      <strong>Cloud Margin Compression:</strong> Q4 operating margin contracted by 180 bps from 24.1% to 22.3% due to expedited server leasing.
                    </li>
                    <li className="demo-finding-item">
                      <strong>Infrastructure Inflation:</strong> Server colocation and electrical utility expenses rose 32% quarter-over-quarter.
                    </li>
                    <li className="demo-finding-item">
                      <strong>Offsetting Factors:</strong> Enterprise seat expansion softened the downside, driving net recurring revenue up 11.4%.
                    </li>
                  </ul>

                  <div className="demo-evidence-preview">
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                      <strong style={{ color: "#e2e8f0" }}>Source: 10K_Annual_Report.pdf</strong>
                      <span style={{ color: "#60a5fa", fontFamily: "var(--font-mono)" }}>Pg 42 · Chunk #108</span>
                    </div>
                    <p style={{ fontStyle: "italic", fontSize: "11px", margin: 0 }}>
                      "...cloud infrastructure operations totaled $48.2M compared to $36.5M in prior quarter, influenced by leasehold commitments..."
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CORE FEATURES GRID */}
      <section id="features" className="landing-section">
        <div className="landing-container">
          <div style={{ textAlign: "center", marginBottom: "50px" }}>
            <span className="section-tagline">Engineered for Precision</span>
            <h2 className="section-title">Built Ground-Up for Deep Financial & Business Context</h2>
            <p className="section-desc" style={{ margin: "0 auto" }}>
              Generic LLM wrappers fail on complex tabular data and multi-page financial filings.
              AIBA solves this with an enterprise-grade document intelligence stack.
            </p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon-wrap">
                <FileCheck size={24} />
              </div>
              <h3>Docling Structural Parsing</h3>
              <p>
                Ingests complex PDF layouts, preserving multi-column formats, table structures, and hierarchical section headers into structured JSON representations.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrap" style={{ background: "rgba(139, 92, 246, 0.15)", color: "#a78bfa" }}>
                <Layers size={24} />
              </div>
              <h3>Hybrid Retrieval (FAISS + BM25)</h3>
              <p>
                Combines dense semantic vector search (BGE embeddings) with sparse lexical keyword matching using Reciprocal Rank Fusion for maximum recall.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrap" style={{ background: "rgba(16, 185, 129, 0.15)", color: "#34d399" }}>
                <Cpu size={24} />
              </div>
              <h3>Cross-Encoder Precision Reranking</h3>
              <p>
                Retrieved chunks undergo deep cross-encoder reordering to ensure only the most authoritative evidence is passed to the generation stage.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrap" style={{ background: "rgba(245, 158, 11, 0.15)", color: "#fbbf24" }}>
                <BarChart3 size={24} />
              </div>
              <h3>Pre-Configured Business Models</h3>
              <p>
                Execute SWOT analyses, segment comparisons, trend projections, root cause isolation, and contribution models directly against your documents.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrap" style={{ background: "rgba(6, 182, 212, 0.15)", color: "#38bdf8" }}>
                <ShieldCheck size={24} />
              </div>
              <h3>Audit-Grade Source Attribution</h3>
              <p>
                Zero black-box assertions. Every analytical claim includes page numbers, chunk identifiers, and cross-encoder relevance scores for auditability.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrap" style={{ background: "rgba(239, 68, 68, 0.15)", color: "#f87171" }}>
                <Zap size={24} />
              </div>
              <h3>Open-Access Workspace</h3>
              <p>
                Zero signup hurdles or authentication bottlenecks. Ingest your documents, interrogate them immediately, and export executive briefs.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CAPABILITIES / FRAMEWORKS TABS */}
      <section id="capabilities" className="landing-section" style={{ background: "rgba(11, 15, 25, 0.6)" }}>
        <div className="landing-container">
          <div style={{ textAlign: "center", marginBottom: "40px" }}>
            <span className="section-tagline">Analytical Frameworks</span>
            <h2 className="section-title">Specialized Strategic Analysis Modules</h2>
            <p className="section-desc" style={{ margin: "0 auto" }}>
              Select a framework to see how AIBA structures business questions into actionable executive intelligence.
            </p>
          </div>

          <div className="capabilities-wrapper">
            <div className="capabilities-tabs">
              {analysisCapabilities.map((cap) => {
                const Icon = cap.icon;
                return (
                  <button
                    key={cap.id}
                    className={`capability-tab-btn ${activeTab === cap.id ? "active" : ""}`}
                    onClick={() => setActiveTab(cap.id)}
                  >
                    <Icon size={16} />
                    <span>{cap.title}</span>
                  </button>
                );
              })}
            </div>

            <div className="capability-tab-content">
              <div className="capability-info">
                <span style={{ fontSize: "12px", color: "#60a5fa", fontWeight: 700, textTransform: "uppercase" }}>
                  {currentCapability.subtitle}
                </span>
                <h3>{currentCapability.title}</h3>
                <p>{currentCapability.description}</p>

                <div className="capability-query-sample">
                  <strong style={{ display: "block", fontSize: "11px", color: "#94a3b8", textTransform: "uppercase", marginBottom: "4px" }}>
                    Sample Interrogation Prompt:
                  </strong>
                  "{currentCapability.sampleQuery}"
                </div>

                <button
                  onClick={() => handleLaunchWithPrompt(currentCapability.sampleQuery)}
                  className="btn btn-primary"
                  style={{ display: "inline-flex" }}
                >
                  <Sparkles size={15} />
                  <span>Run This Analysis in Studio</span>
                  <ArrowRight size={15} />
                </button>
              </div>

              <div className="capability-mockup">
                <div className="mockup-header">
                  <span style={{ fontSize: "11.5px", fontFamily: "var(--font-mono)", color: "#94a3b8" }}>
                    FRAMEWORK: {currentCapability.title.toUpperCase()}
                  </span>
                  <span className="badge badge-success" style={{ fontSize: "10px" }}>
                    SYNTHESIS VERIFIED
                  </span>
                </div>

                <h4 style={{ fontSize: "13px", color: "#60a5fa", textTransform: "uppercase", marginBottom: "8px" }}>
                  Key Findings
                </h4>
                <ul className="demo-findings-list" style={{ marginBottom: "16px" }}>
                  {currentCapability.findings.map((f, i) => (
                    <li key={i} className="demo-finding-item">
                      {f}
                    </li>
                  ))}
                </ul>

                <h4 style={{ fontSize: "13px", color: "#34d399", textTransform: "uppercase", marginBottom: "8px" }}>
                  Executive Conclusion
                </h4>
                <ul className="demo-findings-list" style={{ marginBottom: "16px" }}>
                  {currentCapability.conclusions.map((c, i) => (
                    <li key={i} className="demo-finding-item" style={{ color: "#e2e8f0" }}>
                      {c}
                    </li>
                  ))}
                </ul>

                <div className="demo-evidence-preview" style={{ fontSize: "11px" }}>
                  {currentCapability.evidence}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ARCHITECTURE PIPELINE */}
      <section id="architecture" className="landing-section">
        <div className="landing-container">
          <div style={{ textAlign: "center", marginBottom: "50px" }}>
            <span className="section-tagline">Architectural Integrity</span>
            <h2 className="section-title">The 4-Stage Document Intelligence Pipeline</h2>
            <p className="section-desc" style={{ margin: "0 auto" }}>
              How raw business PDF files are transformed into verified strategic conclusions.
            </p>
          </div>

          <div className="pipeline-grid">
            <div className="pipeline-step-card">
              <span className="pipeline-step-number">STAGE 01</span>
              <h4>Deep Parsing & Structure</h4>
              <p>
                Docling extracts headings, page geometries, and nested tables into semantic hierarchical units with structural awareness.
              </p>
            </div>

            <div className="pipeline-step-card">
              <span className="pipeline-step-number">STAGE 02</span>
              <h4>Dual Vector & Lexical Indexing</h4>
              <p>
                Text chunks are mapped with BGE semantic embeddings in FAISS, while BM25 creates an inverted keyword index for specific numbers & terms.
              </p>
            </div>

            <div className="pipeline-step-card">
              <span className="pipeline-step-number">STAGE 03</span>
              <h4>Hybrid Fusion & Reranking</h4>
              <p>
                Reciprocal Rank Fusion merges dense and sparse scores before a cross-encoder model reranks the top evidence chunks for relevance.
              </p>
            </div>

            <div className="pipeline-step-card">
              <span className="pipeline-step-number">STAGE 04</span>
              <h4>Strategic Business Synthesis</h4>
              <p>
                Configured LLM evaluates question typology, constructs domain prompts, and yields structured findings, conclusions, and citations.
              </p>
            </div>
          </div>

          <div style={{ textAlign: "center", marginTop: "40px" }}>
            <Link to="/methodology" className="hero-btn-secondary" style={{ display: "inline-flex" }}>
              <Cpu size={16} />
              <span>Explore Detailed Pipeline Architecture</span>
              <ArrowRight size={15} />
            </Link>
          </div>
        </div>
      </section>

      {/* FAQ SECTION */}
      <section id="faq" className="landing-section" style={{ background: "rgba(11, 15, 25, 0.4)" }}>
        <div className="landing-container">
          <div style={{ textAlign: "center", marginBottom: "40px" }}>
            <span className="section-tagline">Got Questions?</span>
            <h2 className="section-title">Frequently Asked Questions</h2>
          </div>

          <div className="faq-list">
            {faqs.map((faq, idx) => (
              <div key={idx} className="faq-item">
                <button
                  className="faq-question"
                  onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    size={18}
                    style={{
                      transform: openFaq === idx ? "rotate(180deg)" : "rotate(0deg)",
                      transition: "transform 0.2s",
                      color: "#60a5fa",
                    }}
                  />
                </button>
                {openFaq === idx && (
                  <div className="faq-answer">
                    <p>{faq.a}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA BANNER */}
      <section className="landing-section">
        <div className="landing-container">
          <div className="cta-banner">
            <h2>Ready to Elevate Your Document Intelligence?</h2>
            <p>
              Upload your financial statements, quarterly reports, or strategic decks and begin generating audit-grade business analyses right away.
            </p>
            <div style={{ display: "flex", justifyContent: "center", gap: "16px", flexWrap: "wrap" }}>
              <Link to="/dashboard" className="hero-btn-primary" style={{ padding: "14px 34px" }}>
                <Zap size={18} />
                <span>Launch AIBA Workspace</span>
              </Link>
              <Link to="/knowledge-base" className="hero-btn-secondary" style={{ padding: "14px 28px" }}>
                <Database size={18} />
                <span>Manage Knowledge Base</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="landing-footer">
        <div className="landing-container">
          <div className="footer-inner">
            <div className="footer-brand">
              <div className="landing-brand" style={{ marginBottom: "12px" }}>
                <div className="landing-brand-logo" style={{ width: "32px", height: "32px" }}>
                  <Sparkles size={18} color="#ffffff" />
                </div>
                <span className="landing-brand-name" style={{ fontSize: "18px" }}>AIBA</span>
              </div>
              <p>
                Enterprise-grade RAG AI Business Analyst Agent. Turn complex business PDFs into verifiable evidence-backed intelligence.
              </p>
            </div>

            <div className="footer-links-group">
              <h4>Workspace</h4>
              <ul>
                <li><Link to="/dashboard">Dashboard</Link></li>
                <li><Link to="/chat">AI Assistant Chat</Link></li>
                <li><Link to="/analysis">Business Analysis Studio</Link></li>
                <li><Link to="/knowledge-base">Knowledge Base</Link></li>
                <li><Link to="/reports">Executive Reports</Link></li>
              </ul>
            </div>

            <div className="footer-links-group">
              <h4>Platform</h4>
              <ul>
                <li><Link to="/methodology">RAG Architecture</Link></li>
                <li><Link to="/settings">System Settings</Link></li>
                <li><a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">FastAPI Swagger UI</a></li>
                <li><a href="https://github.com/armaanydv/AIBusinessAnalystAgent" target="_blank" rel="noreferrer">GitHub Repository</a></li>
              </ul>
            </div>

            <div className="footer-links-group">
              <h4>Frameworks</h4>
              <ul>
                <li><a href="#capabilities">Comparative Analysis</a></li>
                <li><a href="#capabilities">SWOT Assessment</a></li>
                <li><a href="#capabilities">Trend & Trajectory</a></li>
                <li><a href="#capabilities">Root Cause Isolation</a></li>
                <li><a href="#capabilities">Contribution Model</a></li>
              </ul>
            </div>
          </div>

          <div className="footer-bottom">
            <span>© {new Date().getFullYear()} AIBA Platform. Open-access Business Intelligence.</span>
            <div style={{ display: "flex", gap: "20px" }}>
              <span>Docling · FAISS · BM25 · BGE · Cross-Encoder</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
