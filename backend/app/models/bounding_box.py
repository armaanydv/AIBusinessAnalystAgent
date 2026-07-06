from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """
    Represents the location of an element on a page.
    Coordinates are measured relative to the page.
    """

    left: float = Field(..., description="Left x-coordinate")
    top: float = Field(..., description="Top y-coordinate")
    right: float = Field(..., description="Right x-coordinate")
    bottom: float = Field(..., description="Bottom y-coordinate")