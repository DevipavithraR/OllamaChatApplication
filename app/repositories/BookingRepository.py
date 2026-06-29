from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.Booking import Booking
from app.repositories.BaseRepository import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, db: Session):
        super().__init__(Booking, db)

    def get_by_customer_id(self, customer_id: int) -> List[Booking]:
        return self.db.query(Booking).filter(Booking.customer_id == customer_id).all()

    def get_active_by_customer_id(self, customer_id: int) -> List[Booking]:
        return self.db.query(Booking).filter(
            and_(
                Booking.customer_id == customer_id,
                Booking.booking_status != "Cancelled"
            )
        ).all()
