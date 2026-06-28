from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MessageResponse(BaseModel):
    sender: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
