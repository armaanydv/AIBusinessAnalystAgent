from pprint import pprint

from docling.document_converter import DocumentConverter

from app.ingestion.mappers.docling_mapper import DoclingMapper


# ==========================================================
# Parse PDF
# ==========================================================

converter = DocumentConverter()

result = converter.convert("sample.pdf")

docling_document = result.document


# ==========================================================
# Map to AIBA
# ==========================================================

mapper = DoclingMapper()

structured_document = mapper.map(docling_document)


# ==========================================================
# Print Result
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT METADATA")
print("=" * 100)

pprint(structured_document.metadata.model_dump())


for page in structured_document.pages:

    print("\n")
    print("=" * 100)
    print(f"PAGE {page.page_number}")
    print("=" * 100)

    for element in page.elements:

        print("-" * 80)

        print(f"Type           : {type(element).__name__}")
        print(f"Reading Order  : {element.reading_order}")

        if hasattr(element, "text"):
            print(f"Text           : {element.text[:100]}")

        if hasattr(element, "headers"):
            print(f"Headers        : {element.headers}")

        print(f"Bounding Box   : {element.bounding_box}")

        print()