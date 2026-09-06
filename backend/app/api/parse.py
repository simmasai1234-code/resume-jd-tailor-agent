from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.services.document_parser import extract_text


router = APIRouter(prefix="/parse", tags=["Document Parser"])

UPLOAD_DIR = Path("uploads")


@router.get("/")
def parse_document(filename: str):
    """
    Extract text from an uploaded PDF or DOCX file.
    """

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    try:
        text = extract_text(str(file_path))

        if not text:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document."
            )

        return {
            "filename": filename,
            "characters": len(text),
            "text": text
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )