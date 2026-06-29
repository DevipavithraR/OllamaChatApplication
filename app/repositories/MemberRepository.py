from sqlalchemy.orm import Session
from typing import Optional
from app.models.Member import Member
from app.repositories.BaseRepository import BaseRepository

class MemberRepository(BaseRepository[Member]):
    def __init__(self, db: Session):
        super().__init__(Member, db)

    def get_by_phone(self, phone: str) -> Optional[Member]:
        return self.db.query(self.model).filter(self.model.phone_number == phone).first()
