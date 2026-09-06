from fastapi import APIRouter

from backend.app.agents.resume_tailoring_agent import ResumeTailoringAgent


router = APIRouter(
    prefix="/tailor",
    tags=["Resume Tailoring"]
)

resume_tailoring_agent = ResumeTailoringAgent()


@router.post("/")
def tailor_resume(
    resume_analysis: dict,
    jd_analysis: dict,
    skill_gap_analysis: dict
):
    """
    Tailor the resume based on the job description
    and identified skill gaps.
    """

    result = resume_tailoring_agent.tailor(
        resume_analysis,
        jd_analysis,
        skill_gap_analysis
    )

    return {
        "message": "Resume tailoring completed",
        "result": result
    }