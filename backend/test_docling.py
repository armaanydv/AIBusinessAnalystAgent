from app.ingestion.ingestion_service import ingestion_service
from app.models.table import Table


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

        print(f"\n\nPage {page.page_number}")
        print("=" * 80)

        for element in page.elements:

            # -----------------------------
            # Tables
            # -----------------------------
            if isinstance(element, Table):

                print("\nTABLE")
                print("-" * 80)

                print(f"Rows    : {element.num_rows}")
                print(f"Columns : {element.num_columns}")

                if element.caption:
                    print(f"Caption : {element.caption}")

                print("\nHeaders")
                print("-" * 80)
                print(element.headers)

                print("\nGrid")
                print("-" * 80)

                for row in element.rows:
                    print(row)

                print("\nRaw Text")
                print("-" * 80)
                print(element.raw_text)

                print("-" * 80)

            # -----------------------------
            # Text / Heading
            # -----------------------------
            else:

                text = getattr(element, "text", "")

                print(
                    f"{type(element).__name__:12} | {text}"
                )

        print("\n")
        print(f"Total Elements : {len(page.elements)}")
        print("=" * 80)


if __name__ == "__main__":
    main()