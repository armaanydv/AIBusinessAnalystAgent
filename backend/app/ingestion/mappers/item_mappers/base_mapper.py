from abc import ABC, abstractmethod

from app.models.bounding_box import BoundingBox


class BaseMapper(ABC):
    """
    Base class for all Docling item mappers.
    Provides common helper methods shared across all mappers.
    """

    @abstractmethod
    def map(self, node, level, reading_order):
        """
        Convert a Docling item into an AIBA DocumentElement.
        """
        pass

    @staticmethod
    def create_bounding_box(prov) -> BoundingBox:
        """
        Convert Docling bounding box to AIBA BoundingBox.
        """

        bbox = prov.bbox

        return BoundingBox(
            left=bbox.l,
            top=bbox.t,
            right=bbox.r,
            bottom=bbox.b,
        )

    @classmethod
    def create_common_fields(cls, prov, reading_order):
        """
        Create fields common to every document element.
        """

        return {
            "page_number": prov.page_no,
            "bounding_box": cls.create_bounding_box(prov),
            "reading_order": reading_order,
        }