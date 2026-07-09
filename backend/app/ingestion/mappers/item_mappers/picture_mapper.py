from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper


class PictureMapper(BaseMapper):

    def map(self, node, level, reading_order):
        return None