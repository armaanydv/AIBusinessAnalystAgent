from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper
from app.models.heading import Heading


class HeadingMapper(BaseMapper):
    """
    Maps a Docling SectionHeaderItem to an AIBA Heading.
    """

    def map(self, node,level, reading_order):

        if not node.prov:
            return None

        prov = node.prov[0]

        return Heading(
            **self.create_common_fields(node,
                prov,
                reading_order,
            ),
            text=node.text,
            level=getattr(node, "level", 1),
        )