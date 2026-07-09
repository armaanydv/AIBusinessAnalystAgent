from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper


class ListMapper(BaseMapper):

    def map(self, node, level, reading_order):
        return None