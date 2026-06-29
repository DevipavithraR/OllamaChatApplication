from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    conversation_id: int
    sender: str
    message: str

class MessageCreate(BaseModel):
    sender: str
    message: str

class MessageResponse(BaseModel):
    message_id: int
    conversation_id: int
    sender: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
