from fastapi import APIRouter
from datetime import datetime
from app.core import get_logger
from app.schemas.responses import HealthResponse

router = APIRouter()
logger = get_logger()

@router.get("/", response_model=HealthResponse)
async def read_root() -> HealthResponse:
    """Root endpoint for basic API status."""
    logger.info("Root endpoint called")
    return HealthResponse(status="ok", message="API is running")

@router.get("/health-check/", response_model=HealthResponse)
async def get_health_check() -> HealthResponse:
    """Detailed health check endpoint."""
    logger.info("Health check endpoint called")
    return HealthResponse(status="healthy", timestamp=datetime.now())