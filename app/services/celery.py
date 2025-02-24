# celery_worker.py
from celery import Celery
import requests
import logging

# Configure Celery
celery_app = Celery(
    'tasks',
)

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task
def invoke_backend():
    url = "http://localhost:8000/v1/process"  # Replace with your FastAPI endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Successfully invoked endpoint: {url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to invoke endpoint: {e}")