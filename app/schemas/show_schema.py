from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.movie_schema import MovieResponse
from app.schemas.theatre_schema import TheatreResponse

class ShowCreate(BaseModel):
    movie_id: int
    theatre_id: int
    screen_number: int
    show_datetime: datetime
    ticket_price: float
    available_seats: int
    total_seats: int

class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    theatre_id: Optional[int] = None
    screen_number: Optional[int] = None
    show_datetime: Optional[datetime] = None
    ticket_price: Optional[float] = None
    available_seats: Optional[int] = None
    total_seats: Optional[int] = None

class ShowResponse(BaseModel):
    show_id: int
    movie_id: int
    theatre_id: int
    screen_number: int
    show_datetime: datetime
    ticket_price: float
    available_seats: int
    total_seats: int
    created_at: datetime
    movie: Optional[MovieResponse] = None
    theatre: Optional[TheatreResponse] = None

    model_config = ConfigDict(from_attributes=True)
