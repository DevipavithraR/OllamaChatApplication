from typing import Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.repositories.BaseRepository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.session_id == session_id).first()

    def link_member(self, conversation_id: int, member_id: int) -> Conversation:
        conversation = self.get(conversation_id)
        if conversation:
            conversation.member_id = member_id
            self.db.commit()
            self.db.refresh(conversation)
        return conversation
