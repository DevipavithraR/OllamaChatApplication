from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TheatreCreate(BaseModel):
    theatre_name: str
    location: str
    screens: Optional[int] = 1

class TheatreUpdate(BaseModel):
    theatre_name: Optional[str] = None
    location: Optional[str] = None
    screens: Optional[int] = None

class TheatreResponse(BaseModel):
    theatre_id: int
    theatre_name: str
    location: str
    screens: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
