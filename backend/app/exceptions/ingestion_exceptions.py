"""
Custom exceptions for the document ingestion layer.
"""


class IngestionError(Exception):
    """
    Base exception for document ingestion errors.
    """


class EmptyDocumentError(IngestionError):
    """
    Raised when a document produces no ingestible content.
    """