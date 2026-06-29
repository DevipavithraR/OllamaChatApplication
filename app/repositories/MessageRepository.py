from sqlalchemy.orm import Session
from app.models.Message import Message
from app.repositories.BaseRepository import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def get_by_conversation_id(self, conversation_id: int):
        return self.db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
