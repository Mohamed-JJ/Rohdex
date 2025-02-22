from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

# add your response schemas here

class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    message: Optional[str] = None
    timestamp: Optional[datetime] = None

