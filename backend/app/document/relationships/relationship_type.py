from enum import Enum


class RelationshipType(str, Enum):
    """
    Types of relationships between document elements.
    """

    CONTAINS = "contains"

    CAPTION = "caption"

    REFERENCE = "reference"

    FOOTNOTE = "footnote"