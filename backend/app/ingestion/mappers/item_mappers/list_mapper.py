from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper
from app.models.list_item import ListItem


class ListMapper(BaseMapper):

    def map(self, node, level, reading_order):

        if not node.prov:
            return None

        prov = node.prov[0]

        hyperlink = None

        if node.hyperlink:
            hyperlink = str(node.hyperlink)

        return ListItem(
            **self.create_common_fields(prov, reading_order),
            text=node.text,
            marker=node.marker,
            enumerated=node.enumerated,
            hyperlink=hyperlink,
        )