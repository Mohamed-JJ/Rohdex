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
    date: str = Field(..., description="date of the entry")
    time: str = Field(..., description="Time of the entry")
    partie_number: str = Field(..., description="partie identifier")
    unit_type: str = Field(..., description="Type of unit")
    quantity: int = Field(..., description="Integer value representing quantity")
    reference: str = Field(..., description="Reference identifier")
    value1: float = Field(..., description="First value measurement")
    value2: float = Field(..., description="Second value measurement")
    value3: float = Field(..., description="Second value measurement")
    weight1: float = Field(..., description="First weight measurement")
    weight2: float = Field(..., description="Second weight measurement")

class PartieEntries(BaseModel):
    entries: List[PartieEntry] = Field(..., description="entries of partie entries")

class Wahrheitsdatei(BaseModel):
    partie_numbers: str = Field(..., description="Must match Partie file identifiers")
    product_descriptions: str = Field(..., description="Text descriptions of down/feather types")
    container_numbers: str = Field(..., description="Unique container identifiers")
    destination: str = Field("Los Angeles", description='Always "Los Angeles" for this client')

class WebHook(BaseModel):
  _id: str
  date: str
  subject: str
  from_email: str
  from_name: str