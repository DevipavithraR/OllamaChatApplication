from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.member import Member
from app.repositories.MemberRepository import MemberRepository
from app.schemas.member_schema import MemberCreate, MemberUpdate
from fastapi import HTTPException, status

class MemberService:
    def __init__(self, db: Session):
        self.repository = MemberRepository(db)

    def create_member(self, member_in: MemberCreate) -> Member:
        """
        Create a new member. Raises HTTP 400 if the phone number already exists.
        """
        existing = self.repository.get_by_phone(member_in.phone_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Member with phone number {member_in.phone_number} already exists."
            )
        
        reg_date = member_in.registration_date or date.today()
        member = Member(
            name=member_in.name,
            phone_number=member_in.phone_number,
            email=member_in.email,
            membership_type=member_in.membership_type,
            registration_date=reg_date
        )
        return self.repository.create(member)

    def get_member_by_id(self, member_id: int) -> Member:
        """
        Get member by ID. Raises 404 if not found.
        """
        member = self.repository.get(member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member with ID {member_id} not found."
            )
        return member

    def get_member_by_phone(self, phone: str) -> Optional[Member]:
        """
        Retrieve member by phone number.
        """
        return self.repository.get_by_phone(phone)

    def get_all_members(self, skip: int = 0, limit: int = 100) -> List[Member]:
        """
        Retrieve a paginated list of members.
        """
        return self.repository.get_all(skip, limit)

    def update_member(self, member_id: int, member_in: MemberUpdate) -> Member:
        """
        Update an existing member.
        """
        member = self.get_member_by_id(member_id)
        update_data = member_in.model_dump(exclude_unset=True)
        
        # If phone is changing, verify uniqueness
        if "phone_number" in update_data and update_data["phone_number"] != member.phone_number:
            existing = self.repository.get_by_phone(update_data["phone_number"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Member with phone number {update_data['phone_number']} already exists."
                )

        return self.repository.update(member, update_data)

    def delete_member(self, member_id: int) -> Member:
        """
        Delete a member by ID.
        """
        member = self.get_member_by_id(member_id)
        return self.repository.delete(member_id)
