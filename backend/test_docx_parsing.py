from docling.document_converter import DocumentConverter


file_path = r"C:\Users\armaa\Downloads\aiba_sample_business_report.docx"


converter = DocumentConverter()

result = converter.convert(file_path)

document = result.document


print("\nDOCUMENT NAME:")
print(document.name)

print("\nTOTAL PAGES:")
print(document.num_pages())

print("\nITEMS:")
print("-" * 60)


for node, level in document.iterate_items():

    print("TYPE:", type(node).__name__)

    print("HAS PROV:", bool(node.prov))

    print("PROV:", node.prov)

    if hasattr(node, "text"):
        print("TEXT:", node.text)

    print("-" * 60)