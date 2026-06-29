from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.message_schema import MessageResponse

class ConversationBase(BaseModel):
    session_id: str
    member_id: Optional[int] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationHistoryResponse(ConversationResponse):
    messages: List[MessageResponse]

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    member_id: Optional[int] = None

