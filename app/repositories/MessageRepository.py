from typing import List
from sqlalchemy.orm import Session
from app.models.Message import Message
from app.repositories.BaseRepository import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def get_last_n_messages(self, conversation_id: int, limit: int = 10) -> List[Message]:
        """
        Retrieve the last N messages for a conversation, ordered chronologically.
        """
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        # Reverse to return in chronological order (oldest to newest)
        return messages[::-1]

    def add_message(self, conversation_id: int, sender: str, message: str) -> Message:
        """
        Add a message to a conversation.
        """
        db_message = Message(
            conversation_id=conversation_id,
            sender=sender,
            message=message
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
