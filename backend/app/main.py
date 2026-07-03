from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Business Analyst API",
    description="Backend API for the AI Business Analyst Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Business Analyst API"
    }


app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)