from sqlalchemy.orm import Session
from app.models.Message import Message
from app.repositories.BaseRepository import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)
