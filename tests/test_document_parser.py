from pathlib import Path

import pytest

from backend.app.services.document_parser import (
    extract_text
)


def test_unsupported_file():

    with pytest.raises(ValueError):

        extract_text(
            "example.txt"
        )


def test_missing_file():

    with pytest.raises(
        FileNotFoundError
    ):

        extract_text(
            "missing.pdf"
        )