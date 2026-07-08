from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("sample.pdf")

doc = result.document

for index, item in enumerate(doc.iterate_items()):

    # iterate_items returns (item, level)
    node, level = item

    print("=" * 80)
    print(f"Index : {index}")
    print(f"Level : {level}")
    print(f"Type  : {type(node).__name__}")
    print(f"Label : {node.label}")

    if node.prov:
        print(f"Page  : {node.prov[0].page_no}")

    if hasattr(node, "text"):
        print(f"Text  : {node.text[:80]}")

    if index == 20:
        break