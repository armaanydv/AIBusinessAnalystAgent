# ==============================================================================
# AIBA BACKEND DOCKERFILE
# Production container for FastAPI + Docling + FAISS + PyTorch RAG Pipeline
# Supports Local Docker, Hugging Face Spaces (16GB RAM), and Cloud VPS
# ==============================================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/cache/huggingface \
    TORCH_HOME=/app/cache/torch \
    STORAGE_ROOT_DIRECTORY=/app/storage/documents \
    PORT=8000

# Install system dependencies required for Docling, RapidOCR, PyMuPDF, and PyTorch
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifest first for Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY app /app/app

# Create necessary persistent directories for storage and model caches
RUN mkdir -p /app/storage/documents /app/cache/huggingface /app/cache/torch

# Expose API ports (8000 for standard Docker / VPS, 7860 for Hugging Face Spaces)
EXPOSE 8000 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start FastAPI server dynamically binding to $PORT (defaults to 8000)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
