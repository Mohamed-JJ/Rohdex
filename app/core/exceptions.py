from fastapi import HTTPException
from .logger import get_logger

logger = get_logger()


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        logger.error(f"[red]Error {status_code}:[/red] {message}")
        super().__init__(self.message)


class FirefliesError(APIError):
    """Exception for Fireflies API errors."""

    pass


class AirtableError(APIError):
    """Exception for Airtable API errors."""

    pass


class OpenAIError(APIError):
    """Exception for OpenAI API errors."""

    pass


def handle_api_error(e: Exception) -> HTTPException:
    """Convert various exceptions to HTTPException."""
    if isinstance(e, HTTPException):
        return e
    elif isinstance(e, APIError):
        return HTTPException(status_code=e.status_code, detail=e.message)
    else:
        logger.exception("Unexpected error occurred")
        return HTTPException(status_code=500, detail=str(e))
