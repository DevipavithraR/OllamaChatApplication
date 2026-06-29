from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Clean Code"])
    author: str = Field(..., min_length=1, max_length=100, examples=["Robert C. Martin"])
    category: str = Field(..., min_length=1, max_length=100, examples=["Programming"])
    isbn: str = Field(..., min_length=10, max_length=20, examples=["978-0132350884"])
    publisher: str = Field(..., min_length=1, max_length=100, examples=["Prentice Hall"])
    publication_year: int = Field(..., gt=0, examples=[2008])
    available_copies: int = Field(..., ge=0, examples=[5])
    total_copies: int = Field(..., ge=0, examples=[5])
    description: Optional[str] = Field(None, examples=["A handbook of agile software craftsmanship."])

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    publisher: Optional[str] = Field(None, min_length=1, max_length=100)
    publication_year: Optional[int] = Field(None, gt=0)
    available_copies: Optional[int] = Field(None, ge=0)
    total_copies: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None

class BookResponse(BookBase):
    book_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
