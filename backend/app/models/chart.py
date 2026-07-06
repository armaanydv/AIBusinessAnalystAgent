from typing import Optional

from app.models.picture import Picture


class Chart(Picture):
    """
    Represents a chart or graph extracted from a document.
    """

    chart_type: Optional[str] = None