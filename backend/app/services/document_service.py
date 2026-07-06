from app.validators.upload_validator import validate_upload
from app.ingestion.ingestion_service import ingestion_service


class DocumentService:

    def upload(self):

        if not validate_upload():
            return {
                "message": "Validation failed."
            }

        return ingestion_service.ingest()


document_service = DocumentService()