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
# Print Metadata
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT METADATA")
print("=" * 100)

pprint(structured_document.metadata.model_dump())


# ==========================================================
# Print Pages & Elements
# ==========================================================

for page in structured_document.pages:

    print("\n")
    print("=" * 100)
    print(f"PAGE {page.page_number}")
    print("=" * 100)

    for element in page.elements:

        print("-" * 80)

        print(f"Type           : {type(element).__name__}")
        print(f"ID             : {element.id}")
        print(f"Docling Ref    : {element.docling_ref}")
        print(f"Reading Order  : {element.reading_order}")
        print(f"Page           : {element.page_number}")

        if hasattr(element, "text"):
            print(f"Text           : {element.text[:120]}")

        if hasattr(element, "headers"):
            print(f"Headers        : {element.headers}")

        if hasattr(element, "caption"):
            print(f"Caption        : {element.caption}")

        if hasattr(element, "marker"):
            print(f"Marker         : {element.marker}")

        if hasattr(element, "enumerated"):
            print(f"Enumerated     : {element.enumerated}")

        if hasattr(element, "hyperlink"):
            print(f"Hyperlink      : {element.hyperlink}")

        if hasattr(element, "image_path"):
            print(f"Image Path     : {element.image_path}")

        if hasattr(element, "has_image"):
            print(f"Has Image      : {element.has_image}")

        print(f"Bounding Box   : {element.bounding_box}")

        print()


# ==========================================================
# Print Document Index
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT INDEX")
print("=" * 100)

if structured_document.index is not None:

    print(f"Elements Indexed     : {len(structured_document.index.by_element_id)}")
    print(f"Docling Refs Indexed : {len(structured_document.index.by_docling_ref)}")
    print(f"Pages Indexed        : {len(structured_document.index.by_page)}")

    print("\nIndexed Pages:")

    for page_number, elements in structured_document.index.by_page.items():
        print(f"  Page {page_number}: {len(elements)} elements")

else:

    print("No document index found.")