
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * CENTRALIZED RESPONSE HANDLER
 *
 * Handles JSON responses, text responses, and API errors.
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
      message = data.detail
        .map((error) => error.msg)
        .join(", ");
    } else if (typeof data?.detail === "string") {
      message = data.detail;
    } else if (data?.message) {
      message = data.message;
    }

    throw new Error(message);
  }

  return data;
}

/**
 * KNOWLEDGE BASE APIs
 */

// Fetch all documents from the Knowledge Base.
export async function getKnowledgeBase() {
  const response = await fetch(`${API_BASE_URL}/knowledge-base`);

  return handleResponse(response);
}

// Upload a PDF document.
export async function uploadDocument(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

// Delete a document using its document ID.
export async function deleteDocument(documentId) {
  const response = await fetch(
    `${API_BASE_URL}/knowledge-base/${encodeURIComponent(documentId)}`,
    {
      method: "DELETE",
    }
  );

  return handleResponse(response);
}

/**
 * CHAT API
 */

// Send a question to the AI assistant.
export async function sendChatMessage(query, topK = 5) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
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

// Submit a business analysis query.
export async function analyzeBusiness(query) {
  const response = await fetch(`${API_BASE_URL}/analysis`, {
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
