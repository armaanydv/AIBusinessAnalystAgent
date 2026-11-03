/**
 * AIBA Platform API Service Layer
 * Centralized API communication with the FastAPI backend,
 * response validation, error normalization, and local persistence.
 */

const DEFAULT_API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export function getApiBaseUrl() {
  if (typeof window !== "undefined") {
    const customUrl = localStorage.getItem("aiba_api_url");
    if (customUrl && customUrl.trim()) {
      return customUrl.trim();
    }
  }
  return DEFAULT_API_BASE_URL;
}

export function setApiBaseUrl(url) {
  if (typeof window !== "undefined") {
    if (url && url.trim()) {
      localStorage.setItem("aiba_api_url", url.trim());
    } else {
      localStorage.removeItem("aiba_api_url");
    }
  }
}

/**
 * CENTRALIZED RESPONSE HANDLER
 * Normalizes JSON responses, plain text, and API error formats.
 */
async function handleResponse(response) {
  const responseText = await response.text();
  let data = null;

  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch {
      data = responseText;
    }
  }

  if (!response.ok) {
    let message = "Something went wrong. Please try again.";

    if (typeof data === "string") {
      message = data;
    } else if (Array.isArray(data?.detail)) {
      message = data.detail.map((err) => err.msg).join(", ");
    } else if (typeof data?.detail === "string") {
      message = data.detail;
    } else if (data?.message) {
      message = data.message;
    }

    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

/**
 * SYSTEM HEALTH & STATUS APIs
 */

export async function checkHealth() {
  const baseUrl = getApiBaseUrl();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(`${baseUrl}/health`, {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return await handleResponse(response);
  } catch (err) {
    return { status: "unreachable", error: err.message };
  }
}

export async function getRoot() {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/`);
  return handleResponse(response);
}

/**
 * KNOWLEDGE BASE APIs
 */

// Fetch all documents from the Knowledge Base
export async function getKnowledgeBase() {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/knowledge-base`);
  return handleResponse(response);
}

// Upload a PDF document
export async function uploadDocument(file) {
  const baseUrl = getApiBaseUrl();
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${baseUrl}/upload`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

// Delete a document by ID
export async function deleteDocument(documentId) {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(
    `${baseUrl}/knowledge-base/${encodeURIComponent(documentId)}`,
    {
      method: "DELETE",
    }
  );

  return handleResponse(response);
}

/**
 * CHAT API
 */

// Send a question to the AI assistant
export async function sendChatMessage(query, topK = 5) {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k: topK,
    }),
  });

  return handleResponse(response);
}

/**
 * BUSINESS ANALYSIS API
 */

// Submit a business analysis query
export async function analyzeBusiness(query) {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/analysis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
    }),
  });

  return handleResponse(response);
}

/**
 * PERSISTENT REPORTS STORAGE (LocalStorage)
 */

const REPORTS_STORAGE_KEY = "aiba_saved_reports_v1";

export function getSavedReports() {
  try {
    const raw = localStorage.getItem(REPORTS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveReport(report) {
  try {
    const current = getSavedReports();
    const newEntry = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      ...report,
    };
    const updated = [newEntry, ...current];
    localStorage.setItem(REPORTS_STORAGE_KEY, JSON.stringify(updated));
    return newEntry;
  } catch (err) {
    console.error("Failed to save report to local storage:", err);
    return null;
  }
}

export function deleteSavedReport(id) {
  try {
    const current = getSavedReports();
    const updated = current.filter((item) => item.id !== id);
    localStorage.setItem(REPORTS_STORAGE_KEY, JSON.stringify(updated));
    return true;
  } catch {
    return false;
  }
}

export function clearSavedReports() {
  try {
    localStorage.removeItem(REPORTS_STORAGE_KEY);
    return true;
  } catch {
    return false;
  }
}

/**
 * PERSISTENT CHAT STORAGE (LocalStorage)
 */

const CHAT_STORAGE_KEY = "aiba_chat_history_v1";

export function getSavedChat() {
  try {
    const raw = localStorage.getItem(CHAT_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveChat(messages) {
  try {
    localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messages));
  } catch (err) {
    console.error("Failed to persist chat:", err);
  }
}

export function clearSavedChat() {
  try {
    localStorage.removeItem(CHAT_STORAGE_KEY);
  } catch (err) {
    console.error("Failed to clear chat:", err);
  }
}
