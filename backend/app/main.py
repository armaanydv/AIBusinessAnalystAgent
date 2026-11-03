from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.analysis import router as analysis_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.knowledge_base import router as knowledge_base_router
from app.api.upload import router as upload_router

from app.api.exception_handlers import (
    global_exception_handler,
    ingestion_exception_handler,
    llm_exception_handler,
    output_validation_exception_handler,
    value_error_handler,
)

from app.exceptions.ingestion_exceptions import (
    IngestionError,
)
from app.exceptions.llm_exceptions import LLMError
from app.exceptions.output_validation_exception import (
    OutputValidationException,
)


app = FastAPI(
    title="AI Business Analyst API",
    description="Backend API for the AI Business Analyst Platform",
    version="0.1.0",
)

# CORS configuration supporting localhost, Vercel deployments, and custom env
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env.strip():
    allowed_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Exception Handlers
# ==========================================================

app.add_exception_handler(
    LLMError,
    llm_exception_handler,
)

app.add_exception_handler(
    IngestionError,
    ingestion_exception_handler,
)

app.add_exception_handler(
    OutputValidationException,
    output_validation_exception_handler,
)

app.add_exception_handler(
    ValueError,
    value_error_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ==========================================================
# Routes
# ==========================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Business Analyst API",
        "status": "online",
        "version": "0.1.0"
    }


app.include_router(health_router)

app.include_router(upload_router)

app.include_router(chat_router)

app.include_router(analysis_router)

app.include_router(knowledge_base_router)
