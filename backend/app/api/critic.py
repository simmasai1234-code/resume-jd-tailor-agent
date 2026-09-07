from fastapi import APIRouter

from backend.app.agents.critic_agent import CriticAgent


router = APIRouter(
    prefix="/critic",
    tags=["Resume Critic"]
)

critic_agent = CriticAgent()


@router.post("/")
def evaluate_resume(
    resume_analysis: dict,
    jd_analysis: dict,
    skill_gap_analysis: dict,
    tailored_resume: dict
):
    """
    Evaluate the quality of the tailored resume.
    """

    result = critic_agent.evaluate(
        resume_analysis,
        jd_analysis,
        skill_gap_analysis,
        tailored_resume
    )

    return {
        "message": "Resume evaluation completed",
        "result": result
    }