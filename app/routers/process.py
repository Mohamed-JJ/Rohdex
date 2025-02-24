from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from ..schemas.responses import WebHook
from datetime import datetime
from app.core import get_logger
from ..services.gmail_services import EmailReader
from ..models.runs import read_users as read_runs, save_users as save_run
from rich.console import Console
import pendulum, os, hashlib, hmac

router = APIRouter()
logger = get_logger()
console = Console()

# @router.get("/emails/", response_model=dict)
# async def process_data() -> dict:
#     """Process the incoming emails."""
#     logger.info("Process endpoint called")

#     # the instance of the gmail reader
#     reader = EmailReader()
    
#     # connect the reader
#     reader.connect()

#     # fetch the last run from the db/runs.json until better solution is proposed
#     runss = read_runs()
#     console.print(runss[runss.__len__() - 1])
#     since = datetime.fromisoformat(runss[runss.__len__() - 1]["date"])  # the date of the last time this endpoint was envoked
#     until = datetime.now()  # the current date

#     # test variables
#     # until = datetime(2024, 2, 20)  # February 20th
#     # since = datetime(2024, 2, 18)  # February 18th

#     # fetch the emails from the inbox
#     emails = reader.fetch_emails(since=since, until=until)

#     # save the run in the json file
#     runss.append({"id": runss.__len__() + 1, "date": datetime.now().isoformat()})
#     newRun = save_run(runss)
#     return {"status": "success", "timestamp": datetime.now(), "data": emails}

# @router.get("/emails/", response_model=dict)
# async def process_attachements() -> dict:
#     """Process the incoming emails."""
#     logger.info("Process endpoint called")

#     # the instance of the gmail reader
#     reader = EmailReader()
    
#     # connect the reader
#     reader.connect()

#     # fetch the last run from the db/runs.json until better solution is proposed
#     runss = read_runs()
#     console.print(runss[runss.__len__() - 1])
#     since = datetime.fromisoformat(runss[runss.__len__() - 1]["date"])  # the date of the last time this endpoint was envoked
#     until = datetime.now()  # the current date

#     # test variables
#     # until = datetime(2024, 2, 20)  # February 20th
#     # since = datetime(2024, 2, 18)  # February 18th

#     # fetch the emails from the inbox
#     emails = reader.fetch_emails(since=since, until=until)

#     ## add the attachements processing here, aka partie files

#     # save the run in the json file
#     runss.append({"id": runss.__len__() + 1, "date": datetime.now().isoformat()})
#     newRun = save_run(runss)
#     return {"status": "success", "timestamp": datetime.now(), "data": emails}

webhooks = []

@router.get("/webhook")
async def get_webhook(challenge: dict):
    # args = Request.body()
    # console.print(args)
    print(" * Nylas connected to the webhook!")
    return challenge["challenge"]

def verify_signature(message, key, signature):
  digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
  return hmac.compare_digest(digest, signature)

@router.post("/webhook")
async def post_webhook(request: Request):
    signature = request.headers.get("x-nylas-signature")
    message = await request.body()
    
    is_genuine = verify_signature(
        message=message,
        key=os.environ["WEBHOOK_SECRET"].encode("utf8"),
        signature=signature,
    )

    if not is_genuine:
        raise HTTPException(status_code=401, detail="Signature verification failed!")

    data = await request.json()

    hook = WebHook(
        data["data"]["object"]["id"],
        pendulum.from_timestamp(
            data["data"]["object"]["date"], tz=pendulum.now().timezone.name
        ).strftime("%d/%m/%Y %H:%M:%S"),
        data["data"]["object"]["subject"],
        data["data"]["object"]["from"][0]["email"],
        data["data"]["object"]["from"][0]["name"],
    )

    webhooks.append(hook)
    
    return PlainTextResponse("Webhook received", status_code=200)