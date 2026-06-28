from typing import Optional
from sqlalchemy.orm import Session
from app.models.Conversation import Conversation
from app.repositories.BaseRepository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session):
        super().__init__(Conversation, db)

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve conversation by session_id.
        """
        return self.db.query(Conversation).filter(Conversation.session_id == session_id).first()

    def link_patient(self, conversation_id: int, patient_id: int) -> Conversation:
        """
        Associate a patient with an active conversation.
        """
        conversation = self.get(conversation_id)
        if conversation:
            conversation.patient_id = patient_id
            self.db.commit()
            self.db.refresh(conversation)
        return conversation
