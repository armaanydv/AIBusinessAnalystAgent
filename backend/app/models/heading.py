from app.models.text_block import TextBlock


class Heading(TextBlock):
    """
    Represents a document heading.
    """

    level: int