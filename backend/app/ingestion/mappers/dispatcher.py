from docling_core.types.doc import (
    ListItem,
    PictureItem,
    SectionHeaderItem,
    TableItem,
    TextItem,
)

from app.ingestion.mappers.item_mappers.heading_mapper import HeadingMapper
from app.ingestion.mappers.item_mappers.table_mapper import TableMapper
from app.ingestion.mappers.item_mappers.text_mapper import TextMapper


class Dispatcher:

    def __init__(self):

        self.heading_mapper = HeadingMapper()
        self.text_mapper = TextMapper()
        self.table_mapper = TableMapper()

    def dispatch(self, node, reading_order):

        if isinstance(node, SectionHeaderItem):
            return self.heading_mapper.map(node, reading_order)

        if isinstance(node, TextItem):
            return self.text_mapper.map(node, reading_order)

        if isinstance(node, TableItem):
            return self.table_mapper.map(node, reading_order)

        # TODO
        if isinstance(node, PictureItem):
            return None

        # TODO
        if isinstance(node, ListItem):
            return None

        return None