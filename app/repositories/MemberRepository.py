from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.member import Member
from app.repositories.BaseRepository import BaseRepository

class MemberRepository(BaseRepository[Member]):
    def __init__(self, db: Session):
        super().__init__(Member, db)

    def get_by_phone(self, phone_number: str) -> Optional[Member]:
        return self.db.query(Member).filter(Member.phone_number == phone_number).first()

    def search_by_name(self, name: str) -> List[Member]:
        return self.db.query(Member).filter(Member.name.ilike(f"%{name}%")).all()
