from app.ingestion.ingestion_service import ingestion_service


def main():

    document = ingestion_service.ingest("sample.pdf")

    print("\n==============================")
    print("STRUCTURED DOCUMENT")
    print("==============================")

    print(f"Title       : {document.metadata.title}")
    print(f"Pages       : {document.metadata.total_pages}")
    print(f"Document ID : {document.metadata.document_id}")

    print("\n==============================")
    print("PAGE CONTENT")
    print("==============================")

    for page in document.pages:

        print(f"\nPage {page.page_number}")
        print("-" * 40)

        for element in page.elements:

            print(
                f"{type(element).__name__:12} | "
                f"{getattr(element, 'text', '')}"
            )


if __name__ == "__main__":
    main()