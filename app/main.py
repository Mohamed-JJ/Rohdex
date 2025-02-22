from fastapi import FastAPI, Request
from app.core import get_logger, handle_api_error
from .routers import health, process
import time

# Initialize components
logger = get_logger()
app = FastAPI(
    title="Shared CRM",
    description="API for processing call transcripts and managing CRM data",
    version="1.0.0",
)

# Add middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"[green]{request.method}[/green] {request.url.path} "
            f"completed in {process_time:.2f}s - {response.status_code}"
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.exception(
            f"[red]Request failed[/red] {request.method} {request.url.path} "
            f"after {process_time:.2f}s"
        )
        raise handle_api_error(e)

# Include routers
app.include_router(health.router, prefix="/v1", tags=["health"])
app.include_router(process.router, prefix="/v1", tags=["process"])