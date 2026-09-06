from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.agents.resume_agent import ResumeAgent
from backend.app.services.document_parser import extract_text


router = APIRouter(
    prefix="/resume",
    tags=["Resume Analysis"]
)

UPLOAD_DIR = Path("uploads").resolve()

resume_agent = ResumeAgent()


@router.get("/analyze")
def analyze_resume(filename: str):

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
            detail="Resume file not found."
        )

    try:
        text = extract_text(str(file_path))

        if not text:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the resume."
            )

        analysis = resume_agent.analyze(text)

        return {
            "filename": filename,
            "analysis": analysis
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )