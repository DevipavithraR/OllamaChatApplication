from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.models.customer import Customer
from app.repositories.base import BaseRepository

class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self, db: Session):
        super().__init__(Reservation, db)

    def get_by_customer_id(self, customer_id: int) -> List[Reservation]:
        """
        Retrieve all reservations for a specific customer ID.
        """
        return self.db.query(Reservation).filter(Reservation.customer_id == customer_id).order_by(Reservation.reservation_time.desc()).all()

    def get_by_customer_phone(self, phone: str) -> List[Reservation]:
        """
        Retrieve all reservations for a customer looked up by phone number.
        """
        return (
            self.db.query(Reservation)
            .join(Customer)
            .filter(Customer.phone == phone)
            .order_by(Reservation.reservation_time.desc())
            .all()
        )

    def get_upcoming_reservations_for_customer(self, customer_id: int) -> List[Reservation]:
        """
        Retrieve upcoming reservations (time >= now) for a customer that are not cancelled.
        """
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.customer_id == customer_id,
                Reservation.reservation_time >= datetime.utcnow(),
                Reservation.status != "CANCELLED"
            )
            .order_by(Reservation.reservation_time.asc())
            .all()
        )
