import re


class BM25Tokenizer:
    """
    Tokenizer used by the BM25 retrieval pipeline.

    Performs lightweight normalization suitable for lexical
    retrieval by:
    - converting text to lowercase
    - removing punctuation
    - collapsing consecutive whitespace
    - splitting text into tokens
    """

    _PUNCTUATION_PATTERN = re.compile(
        r"[^\w\s]"
    )

    _WHITESPACE_PATTERN = re.compile(
        r"\s+"
    )

    def tokenize(
        self,
        text: str,
    ) -> list[str]:
        """
        Convert text into normalized tokens.

        Args:
            text:
                Input text.

        Returns:
            List of normalized tokens.
        """

        if not text:
            return []

        text = text.lower()

        text = self._PUNCTUATION_PATTERN.sub(
            " ",
            text,
        )

        text = self._WHITESPACE_PATTERN.sub(
            " ",
            text,
        ).strip()

        return text.split()