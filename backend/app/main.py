from fastapi import FastAPI

from backend.app.api.upload import router as upload_router
from backend.app.api.parse import router as parse_router
from backend.app.api.jd import router as jd_router
from backend.app.api.resume import router as resume_router
from backend.app.api.matching import router as matching_router
from backend.app.api.skill_gap import router as skill_gap_router


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