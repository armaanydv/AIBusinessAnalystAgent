import { useLocation } from "react-router-dom";

const pageDetails = {
  "/chat": {
    title: "AI Assistant",
    description: "Ask questions about your business documents.",
  },
  "/knowledge-base": {
    title: "Knowledge Base",
    description: "Manage and explore your uploaded documents.",
  },
  "/analysis": {
    title: "Business Analysis",
    description: "Generate insights from your business data.",
  },
};

function Header() {
  const location = useLocation();

  const currentPage = pageDetails[location.pathname] || {
    title: "AIBA Workspace",
    description: "Your AI-powered business intelligence workspace.",
  };

  return (
    <header className="app-header">
      <div className="header-title">
        <h1>{currentPage.title}</h1>
        <p>{currentPage.description}</p>
      </div>

      <div className="header-actions">
        <span className="header-product-label">
          AI Business Analyst
        </span>
      </div>
    </header>
  );
}

export default Header;