from fastapi import APIRouter, HTTPException

from backend.app.agents.jd_agent import JDAgent
from backend.app.services.document_parser import extract_text


router = APIRouter(
    prefix="/jd",
    tags=["JD Analysis"]
)

jd_agent = JDAgent()


@router.get("/analyze")
def analyze_jd(filename: str):

    try:
        text = extract_text(f"uploads/{filename}")

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

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="JD file not found."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )