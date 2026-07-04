from app.models.structured_document import StructuredDocument


class DoclingMapper:

    def map(self, docling_document):

       print(type(docling_document))
       print(dir(docling_document))

       return StructuredDocument()