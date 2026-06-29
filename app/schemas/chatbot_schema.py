from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.message_schema import MessageResponse

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    customer_id: Optional[int] = None

class ConversationResponse(BaseModel):
    conversation_id: int
    session_id: str
    customer_id: Optional[int] = None
    created_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

# Alias for compatibility
ConversationHistoryResponse = ConversationResponse
