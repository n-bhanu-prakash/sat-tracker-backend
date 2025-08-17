from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime

# Generic envelope
class APIMessage(BaseModel):
    message: str

# Request models
class Observer(BaseModel):
    lat: float
    lng: float
    alt: float = Field(..., description="Altitude (meters)")

class PositionsQuery(Observer):
    seconds: int = Field(..., gt=0, le=3600)

class PassesQuery(Observer):
    days: int = Field(..., gt=0, le=10)
    min_visibility: int = Field(0, ge=0, le=3600, description="For visualpasses: min visibility seconds")

class AboveQuery(Observer):
    radius: int = Field(..., gt=0, le=90, description="Search radius in degrees")
    category_id: int = Field(0, description="0=All; see N2YO docs for categories")

# Response models (light typing; we pass through N2YO payloads)
class TLEResponse(BaseModel):
    norad_id: int
    fetched_at: datetime
    payload: Dict[str, Any]

class GenericN2YOResponse(BaseModel):
    payload: Dict[str, Any]
    cached: bool = False
    cached_at: Optional[datetime] = None
