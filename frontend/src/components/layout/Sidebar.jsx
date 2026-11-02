import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    path: "/chat",
    label: "Chat",
    icon: "💬",
  },
  {
    path: "/knowledge-base",
    label: "Knowledge Base",
    icon: "📚",
  },
  {
    path: "/analysis",
    label: "Analysis",
    icon: "📊",
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">A</div>

        <div className="logo-text">
          <h2>AIBA</h2>
          <span>Business Intelligence</span>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-section-title">WORKSPACE</p>

        <nav className="sidebar-nav">
          {navigationItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
              }
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-footer-logo">AI</div>

        <div>
          <p>AIBA Platform</p>
          <span>Intelligent Analysis</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;