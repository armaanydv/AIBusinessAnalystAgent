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
# Map Document
# ==========================================================

mapper = DoclingMapper()

structured_document = mapper.map(docling_document)


# ==========================================================
# Metadata
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT METADATA")
print("=" * 100)

pprint(structured_document.metadata.model_dump())


# ==========================================================
# Pages
# ==========================================================

for page in structured_document.pages:

    print("\n")
    print("=" * 100)
    print(f"PAGE {page.page_number}")
    print("=" * 100)

    for element in page.elements:

        print("-" * 80)

        print(f"Type          : {type(element).__name__}")
        print(f"Reading Order : {element.reading_order}")
        print(f"Docling Ref   : {element.docling_ref}")

        if hasattr(element, "text"):
            print(f"Text          : {element.text}")

        print()


# ==========================================================
# Document Index
# ==========================================================

print("\n")
print("=" * 100)
print("DOCUMENT INDEX")
print("=" * 100)

if structured_document.index is not None:

    print(f"Elements      : {len(structured_document.index.by_element_id)}")
    print(f"Docling Refs  : {len(structured_document.index.by_docling_ref)}")
    print(f"Pages         : {len(structured_document.index.by_page)}")


# ==========================================================
# Relationship Graph
# ==========================================================

print("\n")
print("=" * 100)
print("RELATIONSHIP GRAPH")
print("=" * 100)

if structured_document.relationship_graph is not None:

    print(
        f"Relationships : {len(structured_document.relationship_graph.relationships)}"
    )


# ==========================================================
# Hierarchy Tree
# ==========================================================

print("\n")
print("=" * 100)
print("HIERARCHY TREE")
print("=" * 100)


def print_tree(node, depth=0):

    indent = "    " * depth

    if node.element is None:
        print(f"{indent}ROOT")

    else:

        print(f"{indent}{type(node.element).__name__}")

        if hasattr(node.element, "text"):
            print(f"{indent}  {node.element.text}")

    for child in node.children:
        print_tree(child, depth + 1)


if structured_document.hierarchy_tree is not None:

    print_tree(structured_document.hierarchy_tree.root)

else:

    print("Hierarchy not found.")