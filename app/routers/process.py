from fastapi import APIRouter
from datetime import datetime
from app.core import get_logger
from ..services.gmail_services import EmailReader
from ..models.runs import read_users as read_runs, save_users as save_run
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

    # fetch the last run from the db/runs.json until better solution is proposed
    runss = read_runs()
    console.print(runss[runss.__len__() - 1])
    since = datetime.fromisoformat(runss[runss.__len__() - 1]["date"])  # the date of the last time this endpoint was envoked
    until = datetime.now()  # the current date

    # test variables
    # until = datetime(2024, 2, 20)  # February 20th
    # since = datetime(2024, 2, 18)  # February 18th

    # fetch the emails from the inbox
    emails = reader.fetch_emails(since=since, until=until)

    # save the run in the json file
    runss.append({"id": runss.__len__() + 1, "date": datetime.now().isoformat()})
    newRun = save_run(runss)
    return {"status": "success", "timestamp": datetime.now(), "data": emails}

@router.get("/emails/", response_model=dict)
async def process_attachements() -> dict:
    """Process the incoming emails."""
    logger.info("Process endpoint called")

    # the instance of the gmail reader
    reader = EmailReader()
    
    # connect the reader
    reader.connect()

    # fetch the last run from the db/runs.json until better solution is proposed
    runss = read_runs()
    console.print(runss[runss.__len__() - 1])
    since = datetime.fromisoformat(runss[runss.__len__() - 1]["date"])  # the date of the last time this endpoint was envoked
    until = datetime.now()  # the current date

    # test variables
    # until = datetime(2024, 2, 20)  # February 20th
    # since = datetime(2024, 2, 18)  # February 18th

    # fetch the emails from the inbox
    emails = reader.fetch_emails(since=since, until=until)

    # save the run in the json file
    runss.append({"id": runss.__len__() + 1, "date": datetime.now().isoformat()})
    newRun = save_run(runss)
    return {"status": "success", "timestamp": datetime.now(), "data": emails}