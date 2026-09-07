from fastapi import APIRouter

from backend.app.agents.revision_agent import RevisionAgent


router = APIRouter(
    prefix="/revision",
    tags=["Resume Revision"]
)

revision_agent = RevisionAgent()


@router.post("/")
def revise_resume(
    resume_analysis: dict,
    jd_analysis: dict,
    skill_gap_analysis: dict,
    tailored_resume: dict,
    critic_result: dict
):
    """
    Revise the tailored resume based on critic feedback.
    """

    result = revision_agent.revise(
        resume_analysis,
        jd_analysis,
        skill_gap_analysis,
        tailored_resume,
        critic_result
    )

    return {
        "message": "Resume revision completed",
        "result": result
    }