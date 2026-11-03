import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    """Verify that the health check endpoint returns 200 OK and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"


def test_root_endpoint():
    """Verify root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_knowledge_base_listing():
    """Verify knowledge-base endpoint returns a list structure."""
    response = client.get("/knowledge-base")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "total_documents" in data
    assert isinstance(data["documents"], list)


def test_invalid_upload_extension():
    """Verify that uploading a non-PDF file is rejected by validation."""
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"This is not a PDF file", "text/plain")}
    )
    # Upload validator should reject non-PDF files
    assert response.status_code in [400, 422]
