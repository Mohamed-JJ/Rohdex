from fastapi import APIRouter
from datetime import datetime
from app.core import get_logger

router = APIRouter()
logger = get_logger()

@router.get("/emails/", response_model=dict)
async def process_data() -> dict:
    """Process the incoming emails."""
    logger.info("Process endpoint called")
    return {"status": "success", "timestamp": datetime.now()}