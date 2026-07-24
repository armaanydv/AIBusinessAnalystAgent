from copy import deepcopy
import logging

from app.models.structured_document import StructuredDocument
from app.models.text_block import TextBlock

logger = logging.getLogger(__name__)


class DocumentPreprocessor:
    """
    Cleans and normalizes a StructuredDocument before chunking.
    """

    def preprocess(self, document: StructuredDocument) -> StructuredDocument:
        """
        Returns a cleaned copy of the document.
        """

        logger.info("Starting document preprocessing.")

        cleaned_document = deepcopy(document)

        self._remove_empty_text_blocks(cleaned_document)

        logger.info("Document preprocessing completed.")

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

                    logger.debug("Checking TextBlock: %s", element.text)

                    # Remove empty text blocks
                    if element.text.strip() == "":
                        logger.debug("Removed empty TextBlock.")
                        continue

                    # TEMPORARY TEST
                    if element.text == "Department of Higher Education":
                        logger.debug("Removed test TextBlock.")
                        continue

                cleaned_elements.append(element)

            page.elements = cleaned_elements