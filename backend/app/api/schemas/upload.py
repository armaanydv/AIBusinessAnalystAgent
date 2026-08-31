from pydantic import BaseModel


class UploadResponseSchema(BaseModel):
    """
    Response returned after a document is successfully ingested.
    """

    message: str

    document_id: str

    pages: int

    chunks_created: int