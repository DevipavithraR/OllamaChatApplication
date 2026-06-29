from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.Message import Message
from app.repositories.BaseRepository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.session_id == session_id).first()

    def link_customer(self, conversation_id: int, customer_id: int) -> Optional[Conversation]:
        conv = self.get(conversation_id)
        if conv:
            conv.customer_id = customer_id
            self.db.commit()
            self.db.refresh(conv)
        return conv

    def get_last_n_messages(self, conversation_id: int, limit: int = 10) -> List[Message]:
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        return messages[::-1]

    def add_message(self, conversation_id: int, sender: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            message=content
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
