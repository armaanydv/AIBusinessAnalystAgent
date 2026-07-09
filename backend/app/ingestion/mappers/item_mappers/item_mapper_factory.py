from docling_core.types.doc import (
    ListItem,
    PictureItem,
    SectionHeaderItem,
    TableItem,
    TextItem,
)

from app.ingestion.mappers.item_mappers.heading_mapper import HeadingMapper
from app.ingestion.mappers.item_mappers.list_mapper import ListMapper
from app.ingestion.mappers.item_mappers.picture_mapper import PictureMapper
from app.ingestion.mappers.item_mappers.table_mapper import TableMapper
from app.ingestion.mappers.item_mappers.text_mapper import TextMapper


class ItemMapperFactory:

    def __init__(self):

        self._registry = {
            SectionHeaderItem: HeadingMapper(),
            TextItem: TextMapper(),
            TableItem: TableMapper(),
            PictureItem: PictureMapper(),
            ListItem: ListMapper(),
        }

    def get_mapper(self, node):

        return self._registry.get(type(node))