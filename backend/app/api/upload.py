from fastapi import APIRouter
from backend.app.services import document_service

router = APIRouter()


@router.post("/upload")
def upload_pdf():
    return document_service.upload()