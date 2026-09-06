from fastapi import APIRouter

from backend.app.agents.matching_agent import MatchingAgent


router = APIRouter(
    prefix="/match",
    tags=["Matching"]
)

matching_agent = MatchingAgent()


@router.post("/")
def match_resume_with_jd(
    resume_analysis: dict,
    jd_analysis: dict
):
    """
    Match resume analysis against job description analysis.
    """

    result = matching_agent.analyze(
        resume_analysis,
        jd_analysis
    )

    return {
        "message": "Resume and JD matching completed",
        "result": result
    }