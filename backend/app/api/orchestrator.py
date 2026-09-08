from fastapi import APIRouter

from backend.app.orchestrator.agent_orchestrator import AgentOrchestrator


router = APIRouter(
    prefix="/orchestrate",
    tags=["Agent Orchestrator"]
)

orchestrator = AgentOrchestrator()


@router.post("/")
def run_agent_workflow(
    resume_text: str,
    jd_text: str,
    max_revisions: int = 2
):
    """
    Run the complete agentic resume tailoring workflow.
    """

    result = orchestrator.run(
        resume_text=resume_text,
        jd_text=jd_text,
        max_revisions=max_revisions
    )

    return {
        "message": "Agentic resume tailoring workflow completed",
        "result": result
    }