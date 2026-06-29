from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.Conversation import Conversation
from app.models.Message import Message
from app.repositories.BaseRepository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        return self.db.query(self.model).filter(self.model.session_id == session_id).first()

    def link_member(self, conversation_id: int, member_id: int):
        conversation = self.get(conversation_id)
        if conversation:
            conversation.member_id = member_id
            self.db.commit()

    def get_last_n_messages(self, conversation_id: int, limit: int = 10) -> List[Message]:
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.message_id.desc()).limit(limit).all()[::-1]

    def add_message(self, conversation_id: int, sender: str, content: str) -> Message:
        msg = Message(conversation_id=conversation_id, sender=sender, message=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg
