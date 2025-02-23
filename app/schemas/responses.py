from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional, List

# add your response schemas here

class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    message: Optional[str] = None
    timestamp: Optional[datetime] = None

class TestClass(BaseModel):
    model_name: str = Field(description="the model name used to generate the output")
    answer: str = Field(description="the answer generated by the model")

class PartieEntry(BaseModel):
    index: int = Field(..., description="Sequential number")
    date: str = Field(..., description="Date of the entry")
    time: str = Field(..., description="Time of the entry")
    partie_number: str = Field(..., description="Unique identifier")
    quantity: int = Field(..., description="Integer value representing quantity")
    weight: float = Field(..., description="Weight measurement")
    tare: Optional[float] = Field(None, description="Packaging weight (optional)")

class PartieEntries(BaseModel):
    entries: List[PartieEntry] = Field(..., description="entries of partie entries")

class Wahrheitsdatei(BaseModel):
    partie_numbers: str = Field(..., description="Must match Partie file identifiers")
    product_descriptions: str = Field(..., description="Text descriptions of down/feather types")
    container_numbers: str = Field(..., description="Unique container identifiers")
    destination: str = Field("Los Angeles", description='Always "Los Angeles" for this client')