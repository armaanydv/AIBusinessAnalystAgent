from app.ingestion.mappers.item_mappers.base_mapper import BaseMapper
from app.models.table import Table


class TableMapper(BaseMapper):
    """
    Maps a Docling TableItem to an AIBA Table.
    """

    def map(self, node,level, reading_order):

        if not node.prov:
            return None

        prov = node.prov[0]

        rows = [
            [""] * node.data.num_cols
            for _ in range(node.data.num_rows)
        ]

        for cell in node.data.table_cells:

            for r in range(
                cell.start_row_offset_idx,
                cell.start_row_offset_idx + cell.row_span
            ):

                for c in range(
                    cell.start_col_offset_idx,
                    cell.start_col_offset_idx + cell.col_span
                ):

                    rows[r][c] = cell.text

        headers = rows[0] if rows else []

        raw_text = "\n".join(
            " | ".join(row)
            for row in rows
        )

        caption = None

        if node.captions:
            caption = node.captions[0].text

        return Table(
            **self.create_common_fields(
                prov,
                reading_order,
            ),
            headers=headers,
            rows=rows,
            raw_text=raw_text,
            caption=caption,
            num_rows=node.data.num_rows,
            num_columns=node.data.num_cols,
        )