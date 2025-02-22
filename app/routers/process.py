from fastapi import APIRouter
from datetime import datetime
from app.core import get_logger
from ..services.gmail_services import EmailReader
from rich.console import Console

router = APIRouter()
logger = get_logger()
console = Console()

@router.get("/emails/", response_model=dict)
async def process_data() -> dict:
    """Process the incoming emails."""
    logger.info("Process endpoint called")

    # the instance of the gmail reader
    reader = EmailReader()
    
    # connect the reader
    reader.connect()

    # fetch the emails from the inbox
    emails = reader.fetch_emails()

    # print for debugging
    for email in emails : console.print(email)

    return {"status": "success", "timestamp": datetime.now(), "data": emails}