from collections import defaultdict
from pprint import pprint

from docling.document_converter import DocumentConverter


converter = DocumentConverter()
result = converter.convert("sample.pdf")

doc = result.document

seen = defaultdict(bool)

for node, level in doc.iterate_items():

    class_name = type(node).__name__

    if seen[class_name]:
        continue

    seen[class_name] = True

    print("\n")
    print("=" * 120)
    print(f"TYPE  : {class_name}")
    print(f"LEVEL : {level}")
    print("=" * 120)

    print("\nPUBLIC ATTRIBUTES\n")

    for attr in sorted(dir(node)):

        if attr.startswith("_"):
            continue

        try:
            value = getattr(node, attr)

            print(f"{attr}")
            pprint(value)
            print()

        except Exception as e:
            print(f"{attr} : <ERROR : {e}>")