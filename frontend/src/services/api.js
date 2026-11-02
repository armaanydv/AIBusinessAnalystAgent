const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

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
      message = data.detail.map((error) => error.msg).join(", ");
    } else if (typeof data?.detail === "string") {
      message = data.detail;
    } else if (data?.message) {
      message = data.message;
    }

    throw new Error(message);
  }

  return data;
}

export async function getKnowledgeBase() {
  const response = await fetch(`${API_BASE_URL}/knowledge-base`);
  return handleResponse(response);
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

export async function deleteDocument(documentId) {
  const response = await fetch(
    `${API_BASE_URL}/knowledge-base/${encodeURIComponent(documentId)}`,
    {
      method: "DELETE",
    }
  );

  return handleResponse(response);
}