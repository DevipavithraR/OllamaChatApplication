from sqlalchemy.orm import Session
from typing import Optional, List
from app.repositories.MemberRepository import MemberRepository
from app.models.Member import Member
from app.schemas.member_schema import MemberCreate, MemberUpdate

class MemberService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = MemberRepository(db)

    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        return self.repository.get(member_id)

    def get_member_by_phone(self, phone: str) -> Optional[Member]:
        return self.repository.get_by_phone(phone)

    def get_all_members(self, skip: int = 0, limit: int = 100) -> List[Member]:
        return self.repository.get_all(skip, limit)

    def create_member(self, obj_in: MemberCreate) -> Member:
        db_obj = Member(
            name=obj_in.name,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            gender=obj_in.gender,
            age=obj_in.age,
            membership_status=obj_in.membership_status or "ACTIVE"
        )
        return self.repository.create(db_obj)

    def update_member(self, member_id: int, obj_in: MemberUpdate) -> Optional[Member]:
        db_obj = self.get_member_by_id(member_id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        return self.repository.update(db_obj, update_data)

    def delete_member(self, member_id: int) -> Optional[Member]:
        return self.repository.delete(member_id)
