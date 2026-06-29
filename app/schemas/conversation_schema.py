from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, model_validator
from app.schemas.message_schema import MessageResponse

class ConversationBase(BaseModel):
    session_id: str
    member_id: Optional[int] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(BaseModel):
    session_id: str
    member_id: Optional[int] = None
    customer_id: Optional[int] = None
    messages: List[MessageResponse]

    @model_validator(mode="before")
    @classmethod
    def map_member_to_customer(cls, data):
        if not isinstance(data, dict):
            member_id = getattr(data, "member_id", None)
            if member_id is not None:
                setattr(data, "customer_id", member_id)
        else:
            if "member_id" in data and "customer_id" not in data:
                data["customer_id"] = data["member_id"]
        return data

    model_config = ConfigDict(from_attributes=True)
