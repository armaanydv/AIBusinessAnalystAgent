from app.models.formula import Formula
from app.models.heading import Heading
from app.models.list_item import ListItem
from app.models.picture import Picture
from app.models.table import Table
from app.models.text_block import TextBlock


class TextRenderer:
    """
    Converts document elements into LLM-friendly text.
    """

    def render(self, elements: list) -> str:

        parts = []

        for element in elements:

            if isinstance(element, Heading):

                parts.append(f"# {element.text}")

            elif isinstance(element, Table):

                if element.caption:
                    parts.append(f"Table: {element.caption}")

                if element.raw_text:
                    parts.append(element.raw_text)

            elif isinstance(element, Picture):

                if element.caption:
                    parts.append(f"Figure: {element.caption}")
                elif element.alt_text:
                    parts.append(f"Figure: {element.alt_text}")

            elif isinstance(element, ListItem):

                parts.append(f"{element.marker} {element.text}")

            elif isinstance(element, Formula):

                if element.plain_text:
                    parts.append(element.plain_text)
                elif element.latex:
                    parts.append(element.latex)

            elif isinstance(element, TextBlock):

                parts.append(element.text)

        return "\n\n".join(parts)