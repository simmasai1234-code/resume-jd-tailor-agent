from fastapi import FastAPI

from backend.app.api.upload import router as upload_router
from backend.app.api.parse import router as parse_router
from backend.app.api.jd import router as jd_router
from backend.app.api.resume import router as resume_router
from backend.app.api.matching import router as matching_router
from backend.app.api.skill_gap import router as skill_gap_router
from backend.app.api.resume_tailoring import router as resume_tailoring_router
from backend.app.api.cover_letter import router as cover_letter_router
from backend.app.api.critic import router as critic_router
from backend.app.api.revision import router as revision_router
from backend.app.api.interview import router as interview_router
from backend.app.api.orchestrator import router as orchestrator_router
from backend.app.api.end_to_end import router as end_to_end_router

app = FastAPI(
    title="Resume JD Tailor Agent",
    description="Agentic AI system for resume and job description optimization",
    version="0.1.0"
)


app.include_router(upload_router)
app.include_router(parse_router)
app.include_router(jd_router)
app.include_router(resume_router)
app.include_router(matching_router)
app.include_router(skill_gap_router)
app.include_router(resume_tailoring_router)
app.include_router(cover_letter_router)
app.include_router(critic_router)
app.include_router(revision_router)
app.include_router(interview_router)
app.include_router(orchestrator_router)
app.include_router(end_to_end_router)

@app.get("/")
def root():
    return {
        "message": "Resume JD Tailor Agent is running",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }