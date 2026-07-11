from collections import Counter
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
# Print Pages
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
# Document Index
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT INDEX")
print("=" * 100)

index = structured_document.index

if index is not None:

    print(f"Elements Indexed     : {len(index.by_element_id)}")
    print(f"Docling Refs Indexed : {len(index.by_docling_ref)}")
    print(f"Pages Indexed        : {len(index.by_page)}")

    print("\nIndexed Pages")

    for page_number, elements in index.by_page.items():
        print(f"Page {page_number}: {len(elements)} elements")

else:

    print("No document index found.")


# ==========================================================
# Relationship Graph
# ==========================================================

print("\n")
print("=" * 100)
print("RELATIONSHIP GRAPH")
print("=" * 100)

graph = structured_document.relationship_graph

if graph is not None:

    print(f"Total Relationships : {len(graph.relationships)}")

    counts = Counter(
        relationship.relationship_type.value
        for relationship in graph.relationships
    )

    print("\nRelationship Counts")

    if counts:

        for relationship_type, count in counts.items():
            print(f"{relationship_type:<12}: {count}")

    else:

        print("No relationships found.")

    print("\nRelationships")

    for relationship in graph.relationships:

        print("-" * 80)
        print(f"Type      : {relationship.relationship_type.value}")
        print(f"Source ID : {relationship.source_id}")
        print(f"Target ID : {relationship.target_id}")

else:

    print("No relationship graph found.")


# ==========================================================
# DEBUG DOCLING RELATIONSHIPS
# ==========================================================

print("\n")
print("=" * 100)
print("DOCLING RELATIONSHIP DEBUG")
print("=" * 100)

for node, level in docling_document.iterate_items():

    print("-" * 80)

    print(f"Type      : {type(node).__name__}")
    print(f"Self Ref  : {node.self_ref}")

    print(f"Parent    : {getattr(node, 'parent', None)}")
    print(f"Children  : {getattr(node, 'children', None)}")
    print(f"Captions  : {getattr(node, 'captions', None)}")
    print(f"References: {getattr(node, 'references', None)}")
    print(f"Footnotes : {getattr(node, 'footnotes', None)}")