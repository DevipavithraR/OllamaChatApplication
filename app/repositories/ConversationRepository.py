from typing import Optional
from sqlalchemy.orm import Session
from app.models.Conversation import Conversation
from app.repositories.BaseRepository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.session_id == session_id).first()

    def link_student(self, conversation_id: int, student_id: int) -> Optional[Conversation]:
        conv = self.get(conversation_id)
        if conv:
            conv.student_id = student_id
            self.db.commit()
            self.db.refresh(conv)
        return conv
