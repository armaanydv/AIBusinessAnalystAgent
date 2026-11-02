
import { useRef, useState } from "react";
import { sendChatMessage } from "../services/api";
import "./chat.css";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const question = query.trim();

    if (!question || loading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((previous) => [...previous, userMessage]);
    setQuery("");
    setError("");
    setLoading(true);

    try {
      const result = await sendChatMessage(question, 5);

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: result.answer,
        retrievalResults: result.retrieval_results || [],
        llm: result.llm,
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (err) {
      setError(err.message || "Unable to generate a response.");
    } finally {
      setLoading(false);
      setTimeout(scrollToBottom, 100);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  const clearConversation = () => {
    if (loading) return;

    setMessages([]);
    setError("");
  };

  return (
    <section className="chat-page">
      <div className="chat-toolbar">
        <div>
          <h2>AI Business Assistant</h2>
          <p>
            Ask questions and get answers grounded in your Knowledge Base.
          </p>
        </div>

        <button
          className="chat-clear-button"
          onClick={clearConversation}
          disabled={messages.length === 0 || loading}
        >
          Clear conversation
        </button>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <div className="chat-welcome-icon">✦</div>

              <h2>How can I help you today?</h2>

              <p>
                Ask questions about your uploaded business documents.
                I'll retrieve relevant information to support my answers.
              </p>

              <div className="chat-suggestions">
                <button
                  onClick={() =>
                    setQuery("Summarize the key findings in my documents.")
                  }
                >
                  Summarize my documents
                </button>

                <button
                  onClick={() =>
                    setQuery("What are the major business challenges?")
                  }
                >
                  Identify business challenges
                </button>

                <button
                  onClick={() =>
                    setQuery("What important insights can you find?")
                  }
                >
                  Find important insights
                </button>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-message ${message.role}`}
            >
              <div className="chat-avatar">
                {message.role === "user" ? "You" : "AI"}
              </div>

              <div className="chat-message-content">
                <div className="chat-message-heading">
                  <strong>
                    {message.role === "user" ? "You" : "AIBA Assistant"}
                  </strong>
                </div>

                <div className="chat-message-text">
                  {message.content}
                </div>

                {message.role === "assistant" && (
                  <>
                    {message.retrievalResults?.length > 0 && (
                      <details className="chat-evidence">
                        <summary>
                          Supporting evidence (
                          {message.retrievalResults.length})
                        </summary>

                        <div className="chat-evidence-list">
                          {message.retrievalResults.map((item) => (
                            <div
                              className="chat-evidence-card"
                              key={item.chunk_id}
                            >
                              <div className="chat-evidence-header">
                                <strong>
                                  {item.title || "Retrieved document"}
                                </strong>

                                <span>
                                  {item.rerank_score != null
                                    ? `Rerank: ${item.rerank_score.toFixed(3)}`
                                    : item.retrieval_score != null
                                      ? `Retrieval: ${item.retrieval_score.toFixed(3)}`
                                      : "Score unavailable"}
                                </span>
                              </div>

                              <p>{item.text}</p>
                            </div>
                          ))}
                        </div>
                      </details>
                    )}

                    {message.llm && (
                      <div className="chat-usage">
                        <span>
                          Input: {message.llm.input_tokens ?? "—"}
                        </span>
                        <span>
                          Output: {message.llm.output_tokens ?? "—"}
                        </span>
                        <span>
                          Total: {message.llm.total_tokens ?? "—"}
                        </span>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-message assistant">
              <div className="chat-avatar">AI</div>

              <div className="chat-message-content">
                <strong>AIBA Assistant</strong>

                <div className="chat-typing">
                  <span />
                  <span />
                  <span />
                  <p>Analyzing your documents...</p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="chat-error" role="alert">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input-area" onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something about your business documents..."
            rows={1}
            disabled={loading}
          />

          <button
            type="submit"
            disabled={!query.trim() || loading}
          >
            {loading ? "Thinking..." : "Send"}
          </button>

          <p>
            Enter to send · Shift + Enter for a new line
          </p>
        </form>
      </div>
    </section>
  );
}

export default Chat;
