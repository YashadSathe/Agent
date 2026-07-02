from fastapi import APIRouter
from agent.core.config import settings

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():

    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment
    }