from pathlib import Path


ALLOWED_EXTENSIONS = {".pdf"}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


def validate_upload(
    filename: str | None,
    content: bytes,
) -> None:
    """
    Validate an uploaded document.

    Raises:
        ValueError: If the uploaded file is invalid.
    """

    # ---------------------------------------------------------
    # Validate filename
    # ---------------------------------------------------------

    if not filename:
        raise ValueError(
            "Uploaded file must have a filename."
        )

    # ---------------------------------------------------------
    # Validate extension
    # ---------------------------------------------------------

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Currently, only PDF files are supported."
        )

    # ---------------------------------------------------------
    # Validate file content
    # ---------------------------------------------------------

    if not content:
        raise ValueError(
            "Uploaded file is empty."
        )

    # ---------------------------------------------------------
    # Validate file size
    # ---------------------------------------------------------

    if len(content) > MAX_FILE_SIZE:
        raise ValueError(
            "Uploaded file exceeds the maximum "
            "allowed size of 20 MB."
        )