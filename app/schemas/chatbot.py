from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.message_schema import MessageResponse

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100, examples=["session_12345"])
    message: str = Field(..., min_length=1, max_length=2000, examples=["Search books about Clean Code"])

class ChatResponse(BaseModel):
    session_id: str
    response: str
    member_id: Optional[int] = None
    customer_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
