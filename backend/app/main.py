import time
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.logging_config import setup_logging

setup_logging()

from backend.app.logging_config import get_logger
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
from backend.app.api.health import router as health_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Agentic AI system for resume and job description optimization",
    version="0.1.0"
)
logger = get_logger("HTTP")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s | %s | %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Frontend static files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/", include_in_schema=False)
async def frontend():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# --------------------------------------------------
# API Routers
# --------------------------------------------------

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
app.include_router(health_router)