from datetime import datetime, timezone

from fastapi import APIRouter

from backend.app.config import settings


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }