from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
def upload_pdf():
    return {
        "message": "Upload endpoint is working."
    }