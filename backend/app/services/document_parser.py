from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    try:
        document = pymupdf.open(file_path)

        text = []

        try:
            for page in document:
                page_text = page.get_text()

                if page_text:
                    text.append(page_text.strip())
        finally:
            document.close()

        return "\n".join(text).strip()

    except pymupdf.FileNotFoundError as e:
        raise FileNotFoundError(
            f"File not found: {file_path}"
        ) from e


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        content = paragraph.text.strip()

        if content:
            text.append(content)

    return "\n".join(text).strip()


def extract_text(file_path: str) -> str:
    """
    Detect file type and extract text.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        "Unsupported file format. Only PDF and DOCX are supported."
    )