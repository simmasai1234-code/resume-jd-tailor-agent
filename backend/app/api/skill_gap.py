from fastapi import APIRouter

from backend.app.agents.skill_gap_agent import SkillGapAgent


router = APIRouter(
    prefix="/skill-gap",
    tags=["Skill Gap Analysis"]
)

skill_gap_agent = SkillGapAgent()


@router.post("/")
def analyze_skill_gaps(matching_result: dict):
    """
    Analyze skill gaps from resume-JD matching results.
    """

    result = skill_gap_agent.analyze(
        matching_result
    )

    return {
        "message": "Skill gap analysis completed",
        "result": result
    }