from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MessageBase(BaseModel):
    sender: str
    message: str

class MessageResponse(MessageBase):
    message_id: int
    conversation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
