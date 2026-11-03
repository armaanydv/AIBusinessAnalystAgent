import { useEffect, useState } from "react";
import { NavLink, Link } from "react-router-dom";
import {
  LayoutDashboard,
  MessageSquare,
  BarChart3,
  Database,
  FileText,
  Cpu,
  Settings,
  ExternalLink,
  Sparkles,
} from "lucide-react";
import { checkHealth, getKnowledgeBase } from "../../services/api";

const workspaceNavItems = [
  {
    path: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    path: "/chat",
    label: "AI Chat",
    icon: MessageSquare,
  },
  {
    path: "/analysis",
    label: "Business Analysis",
    icon: BarChart3,
  },
  {
    path: "/knowledge-base",
    label: "Knowledge Base",
    icon: Database,
  },
  {
    path: "/reports",
    label: "Executive Reports",
    icon: FileText,
  },
];

const systemNavItems = [
  {
    path: "/methodology",
    label: "RAG Architecture",
    icon: Cpu,
  },
  {
    path: "/settings",
    label: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(null);
  const [docCount, setDocCount] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function checkStatus() {
      try {
        const health = await checkHealth();
        if (mounted) {
          setIsBackendHealthy(health?.status === "healthy");
        }
        const kb = await getKnowledgeBase();
        if (mounted && kb?.total_documents !== undefined) {
          setDocCount(kb.total_documents);
        }
      } catch {
        if (mounted) {
          setIsBackendHealthy(false);
        }
      }
    }

    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <Link to="/" className="sidebar-logo" title="View Public Landing Page">
          <div className="logo-badge">
            <Sparkles size={20} />
          </div>
          <div className="logo-text">
            <h2>AIBA</h2>
            <span>Business Intelligence</span>
          </div>
        </Link>
      </div>

      <div className="sidebar-nav-container">
        <div>
          <p className="sidebar-group-title">WORKSPACE</p>
          <nav className="sidebar-nav">
            {workspaceNavItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    isActive ? "nav-link-item active" : "nav-link-item"
                  }
                >
                  <span className="nav-icon-wrap">
                    <Icon size={17} />
                  </span>
                  <span>{item.label}</span>
                  {item.path === "/knowledge-base" && docCount !== null && (
                    <span className="nav-badge-pill">{docCount}</span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        <div>
          <p className="sidebar-group-title">PLATFORM</p>
          <nav className="sidebar-nav">
            {systemNavItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    isActive ? "nav-link-item active" : "nav-link-item"
                  }
                >
                  <span className="nav-icon-wrap">
                    <Icon size={17} />
                  </span>
                  <span>{item.label}</span>
                </NavLink>
              );
            })}

            <Link to="/" className="nav-link-item" style={{ marginTop: "6px" }}>
              <span className="nav-icon-wrap">
                <ExternalLink size={16} />
              </span>
              <span>Landing Page</span>
            </Link>
          </nav>
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-status-box">
          <div
            className={`status-dot ${isBackendHealthy ? "" : "offline"}`}
            title={isBackendHealthy ? "Backend API Online" : "Backend API Offline"}
          />
          <div className="status-info">
            <p>{isBackendHealthy ? "API Connected" : "Local Backend"}</p>
            <span>{isBackendHealthy ? "RAG Engine Active" : "Port 8000"}</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
