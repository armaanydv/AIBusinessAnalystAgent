from fastapi import APIRouter
from app.services.upload_service import upload_service

router = APIRouter()


@router.post("/upload")
def upload_pdf():
    return upload_service.upload()