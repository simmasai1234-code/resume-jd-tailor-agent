from fastapi import APIRouter

from backend.app.agents.cover_letter_agent import CoverLetterAgent


router = APIRouter(
    prefix="/cover-letter",
    tags=["Cover Letter"]
)

cover_letter_agent = CoverLetterAgent()


@router.post("/")
def generate_cover_letter(
    resume_analysis: dict,
    jd_analysis: dict,
    skill_gap_analysis: dict
):
    """
    Generate a personalized cover letter.
    """

    result = cover_letter_agent.generate(
        resume_analysis,
        jd_analysis,
        skill_gap_analysis
    )

    return {
        "message": "Cover letter generated successfully",
        "result": result
    }