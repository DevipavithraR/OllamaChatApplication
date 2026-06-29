from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.TrainerBooking import TrainerBooking
from app.repositories.BaseRepository import BaseRepository

class TrainerBookingRepository(BaseRepository[TrainerBooking]):
    def __init__(self, db: Session):
        super().__init__(TrainerBooking, db)

    def get_upcoming_bookings_for_member(self, member_id: int) -> List[TrainerBooking]:
        return self.db.query(self.model).filter(
            self.model.member_id == member_id,
            self.model.status == "CONFIRMED",
            self.model.booking_datetime >= datetime.utcnow()
        ).all()

    def get_bookings_by_member_phone(self, phone: str) -> List[TrainerBooking]:
        from app.models.Member import Member
        return self.db.query(self.model).join(Member).filter(
            Member.phone_number == phone
        ).all()
