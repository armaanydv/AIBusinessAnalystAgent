from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper
from app.models.picture import Picture


class PictureMapper(BaseMapper):

    def map(self, node, level, reading_order):

        if not node.prov:
            return None

        prov = node.prov[0]

        caption = None

        if node.captions:
            caption = str(node.captions[0])

        return Picture(
            **self.create_common_fields(prov, reading_order),
            image_path=None,
            caption=caption,
            alt_text=None,
            has_image=node.image is not None,
        )