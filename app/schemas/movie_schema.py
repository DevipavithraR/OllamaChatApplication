from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class MovieCreate(BaseModel):
    title: str
    genre: str
    language: str
    duration: str
    rating: str
    description: Optional[str] = None
    release_date: Optional[date] = None

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[str] = None
    rating: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[date] = None

class MovieResponse(BaseModel):
    movie_id: int
    title: str
    genre: str
    language: str
    duration: str
    rating: str
    description: Optional[str] = None
    release_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
