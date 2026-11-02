
import { useState } from "react";
import { analyzeBusiness } from "../services/api";
import "./analysis.css";

function Analysis() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalysis = async (event) => {
    event.preventDefault();

    if (!query.trim()) {
      setError("Please enter a business analysis question.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await analyzeBusiness(query.trim());
      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to generate business analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analysis-page">
      <section className="analysis-intro">
        <h2>Business Analysis</h2>
        <p>
          Ask business-related questions about your uploaded documents.
          AIBA will retrieve relevant information and generate structured
          analytical findings.
        </p>
      </section>

      <form className="analysis-form" onSubmit={handleAnalysis}>
        <label htmlFor="analysis-query">
          What would you like to analyze?
        </label>

        <textarea
          id="analysis-query"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Example: Compare the revenue performance of different business segments."
          rows={4}
          disabled={loading}
        />

        <div className="analysis-form-footer">
          <span>Be specific to get more meaningful insights.</span>

          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? "Analyzing..." : "Generate Analysis"}
          </button>
        </div>
      </form>

      {error && (
        <div className="analysis-error">
          {error}
        </div>
      )}

      {loading && (
        <div className="analysis-loading">
          <div className="analysis-spinner"></div>
          <p>Analyzing your documents...</p>
          <span>Retrieving evidence and generating insights.</span>
        </div>
      )}

      {!loading && !result && !error && (
        <div className="analysis-empty">
          <div className="analysis-empty-icon">✦</div>
          <h3>Ready to analyze your business data?</h3>
          <p>
            Enter a question above to generate findings, conclusions,
            and supporting evidence from your knowledge base.
          </p>
        </div>
      )}

      {result && (
        <section className="analysis-results">
          <div className="analysis-results-header">
            <div>
              <span className="section-eyebrow">ANALYSIS RESULT</span>
              <h3>Generated Insights</h3>
            </div>

            <span className="analysis-type">
              {result.analysis_type}
            </span>
          </div>

          <div className="analysis-result-section">
            <h4>Key Findings</h4>

            {result.findings?.length ? (
              <ul>
                {result.findings.map((finding, index) => (
                  <li key={index}>{finding}</li>
                ))}
              </ul>
            ) : (
              <p className="no-result">No findings returned.</p>
            )}
          </div>

          <div className="analysis-result-section">
            <h4>Conclusions</h4>

            {result.conclusions?.length ? (
              <ul>
                {result.conclusions.map((conclusion, index) => (
                  <li key={index}>{conclusion}</li>
                ))}
              </ul>
            ) : (
              <p className="no-result">No conclusions returned.</p>
            )}
          </div>

          <div className="analysis-result-section">
            <h4>Supporting Evidence</h4>

            {result.supporting_evidence?.length ? (
              <div className="evidence-list">
                {result.supporting_evidence.map((evidence, index) => (
                  <div className="evidence-item" key={index}>
                    <span className="evidence-number">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <p>{evidence}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-result">No supporting evidence returned.</p>
            )}
          </div>
        </section>
      )}
    </div>
  );
}

export default Analysis;
