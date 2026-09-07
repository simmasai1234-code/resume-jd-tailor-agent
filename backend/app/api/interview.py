from fastapi import APIRouter

from backend.app.agents.interview_agent import InterviewAgent


router = APIRouter(
    prefix="/interview",
    tags=["Interview Preparation"]
)

interview_agent = InterviewAgent()


@router.post("/")
def generate_interview_preparation(
    resume_analysis: dict,
    jd_analysis: dict,
    skill_gap_analysis: dict,
    tailored_resume: dict
):
    """
    Generate personalized interview preparation.
    """

    result = interview_agent.generate(
        resume_analysis,
        jd_analysis,
        skill_gap_analysis,
        tailored_resume
    )

    return {
        "message": "Interview preparation generated successfully",
        "result": result
    }