from typing import List
from sqlalchemy.orm import Session
from app.models.message import Message
from app.repositories.BaseRepository import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def get_last_n_messages(self, conversation_id: int, limit: int = 10) -> List[Message]:
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        return messages[::-1] # return in chronological order

    def add_message(self, conversation_id: int, sender: str, message_text: str) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            sender=sender,
            message=message_text
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg
