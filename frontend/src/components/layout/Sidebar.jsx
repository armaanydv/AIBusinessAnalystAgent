import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>AIBA</h2>
        <span>AI Business Analyst</span>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/chat">Chat</NavLink>
        <NavLink to="/knowledge-base">Knowledge Base</NavLink>
        <NavLink to="/analysis">Analysis</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;