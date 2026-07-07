from copy import deepcopy

from app.models.structured_document import StructuredDocument
from app.models.text_block import TextBlock


class DocumentPreprocessor:
    """
    Cleans and normalizes a StructuredDocument before chunking.
    """

    def preprocess(self, document: StructuredDocument) -> StructuredDocument:
        """
        Returns a cleaned copy of the document.
        """

        print("\n===================================")
        print("DOCUMENT PREPROCESSOR STARTED")
        print("===================================\n")

        cleaned_document = deepcopy(document)

        self._remove_empty_text_blocks(cleaned_document)

        print("\n===================================")
        print("DOCUMENT PREPROCESSOR FINISHED")
        print("===================================\n")

        return cleaned_document

    def _remove_empty_text_blocks(self, document: StructuredDocument) -> None:
        """
        Removes empty text blocks.

        TEMPORARY:
        Also removes one known text block so we can verify
        that preprocessing is actually modifying the document.
        """

        for page in document.pages:

            cleaned_elements = []

            for element in page.elements:

                if isinstance(element, TextBlock):

                    print(f"Checking: {element.text}")

                    # Remove empty text blocks
                    if element.text.strip() == "":
                        print("-> Removed Empty TextBlock")
                        continue

                    # TEMPORARY TEST
                    if element.text == "Department of Higher Education":
                        print("-> Removed Test TextBlock")
                        continue

                cleaned_elements.append(element)

            page.elements = cleaned_elements


document_preprocessor = DocumentPreprocessor()