from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

class MessageBase(BaseModel):
    sender: str
    message: str

class MessageCreate(MessageBase):
    conversation_id: int

class MessageResponse(BaseModel):
    sender: str
    content: str
    created_at: datetime

    @model_validator(mode="before")
    @classmethod
    def map_message_to_content(cls, data):
        if not isinstance(data, dict):
            # SQLAlchemy object
            content = getattr(data, "message", None)
            if content is not None:
                setattr(data, "content", content)
        else:
            if "message" in data and "content" not in data:
                data["content"] = data["message"]
        return data

    model_config = ConfigDict(from_attributes=True)
