from fastapi import FastAPI

app = FastAPI(
    title="Resume JD Tailor Agent",
    description="Agentic AI system for resume and job description optimization",
    version="0.1.0"
)


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
