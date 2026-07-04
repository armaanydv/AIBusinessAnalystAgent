class StructuredDocument:
    """
    Internal representation of a parsed document.
    """

    def __init__(
        self,
        text="",
        headings=None,
        tables=None,
        images=None,
        charts=None,
        numbers=None,
        lists=None,
        captions=None,
        page_numbers=None,
        metadata=None,
    ):
        self.text = text
        self.headings = headings or []
        self.tables = tables or []
        self.images = images or []
        self.charts = charts or []
        self.numbers = numbers or []
        self.lists = lists or []
        self.captions = captions or []
        self.page_numbers = page_numbers or []
        self.metadata = metadata or {}