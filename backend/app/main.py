from fastapi import FastAPI

from backend.app.api.upload import router as upload_router


app = FastAPI(
    title="Resume JD Tailor Agent",
    description="Agentic AI system for resume and job description optimization",
    version="0.1.0"
)


app.include_router(upload_router)


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