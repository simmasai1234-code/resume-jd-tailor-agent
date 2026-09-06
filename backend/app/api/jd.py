from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.agents.jd_agent import JDAgent
from backend.app.services.document_parser import extract_text


router = APIRouter(
    prefix="/jd",
    tags=["JD Analysis"]
)

UPLOAD_DIR = Path("uploads").resolve()

jd_agent = JDAgent()


@router.get("/analyze")
def analyze_jd(filename: str):

    file_path = (UPLOAD_DIR / filename).resolve()

    # Security check
    if UPLOAD_DIR not in file_path.parents:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="JD file not found."
        )

    try:
        text = extract_text(str(file_path))

        if not text:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the JD."
            )

        analysis = jd_agent.analyze(text)

        return {
            "filename": filename,
            "analysis": analysis
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
