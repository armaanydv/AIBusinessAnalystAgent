from app.ingestion.ingestion_service import ingestion_service

document = ingestion_service.ingest("sample.pdf")

print(document)