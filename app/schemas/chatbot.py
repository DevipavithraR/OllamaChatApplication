from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100, examples=["session_12345"])
    message: str = Field(..., min_length=1, max_length=2000, examples=["What is on the menu today?"])

class ChatResponse(BaseModel):
    session_id: str
    response: str
    customer_id: Optional[int] = None

class MessageResponse(BaseModel):
    sender: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    session_id: str
    customer_id: Optional[int] = None
    messages: List[MessageResponse]

    model_config = ConfigDict(from_attributes=True)
