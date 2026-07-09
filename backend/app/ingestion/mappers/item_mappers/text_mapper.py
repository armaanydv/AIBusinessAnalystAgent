from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper
from app.models.text_block import TextBlock


class TextMapper(BaseMapper):
    """
    Maps a Docling TextItem to an AIBA TextBlock.
    """

    def map(self, node,level, reading_order):

        if not node.prov:
            return None

        prov = node.prov[0]

        return TextBlock(
            **self.create_common_fields(
                prov,
                reading_order,
            ),
            text=node.text,
        )