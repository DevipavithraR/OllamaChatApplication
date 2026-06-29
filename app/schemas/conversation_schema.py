from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.message_schema import MessageResponse

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100, examples=["session_12345"])
    message: str = Field(..., min_length=1, max_length=2000, examples=["What B.Tech courses are available?"])

class ChatResponse(BaseModel):
    session_id: str
    response: str
    student_id: Optional[int] = None

class ConversationResponse(BaseModel):
    session_id: str
    student_id: Optional[int] = None
    messages: List[MessageResponse]

    model_config = ConfigDict(from_attributes=True)
