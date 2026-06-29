from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ConversationBase(BaseModel):
    session_id: str
    customer_id: Optional[int] = None

class ConversationResponse(ConversationBase):
    conversation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
