import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/chat";
import KnowledgeBase from "./pages/knowledgebase";
import Analysis from "./pages/analysis";
import Reports from "./pages/Reports";
import Architecture from "./pages/Architecture";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<LandingPage />} />

        {/* Workspace Shell */}
        <Route element={<AppLayout />}>
          <Route path="/app" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/knowledge-base" element={<KnowledgeBase />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/methodology" element={<Architecture />} />
          <Route path="/architecture" element={<Navigate to="/methodology" replace />} />
          <Route path="/settings" element={<Settings />} />
        </Route>

        {/* Catch-all redirect to Landing Page */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
