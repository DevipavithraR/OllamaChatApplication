from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.ServiceBooking import ServiceBooking
from app.models.Customer import Customer
from app.repositories.BaseRepository import BaseRepository

class ServiceBookingRepository(BaseRepository[ServiceBooking]):
    def __init__(self, db: Session):
        super().__init__(ServiceBooking, db)

    def get_by_customer_id(self, customer_id: int) -> List[ServiceBooking]:
        """
        Get all service bookings for a specific customer.
        """
        return (
            self.db.query(ServiceBooking)
            .filter(ServiceBooking.customer_id == customer_id)
            .order_by(ServiceBooking.service_date.desc())
            .all()
        )

    def get_by_customer_phone(self, phone_number: str) -> List[ServiceBooking]:
        """
        Retrieve all service bookings for a customer by their phone number.
        """
        return (
            self.db.query(ServiceBooking)
            .join(Customer)
            .filter(Customer.phone_number == phone_number)
            .order_by(ServiceBooking.service_date.desc())
            .all()
        )

    def get_upcoming_bookings_for_customer(self, customer_id: int) -> List[ServiceBooking]:
        """
        Retrieve upcoming service bookings for a customer.
        """
        return (
            self.db.query(ServiceBooking)
            .filter(
                ServiceBooking.customer_id == customer_id,
                ServiceBooking.service_date >= datetime.utcnow(),
                ServiceBooking.booking_status != "Cancelled"
            )
            .order_by(ServiceBooking.service_date.asc())
            .all()
        )

    def get_by_vehicle_id(self, vehicle_id: int) -> List[ServiceBooking]:
        """
        Retrieve all bookings for a vehicle.
        """
        return (
            self.db.query(ServiceBooking)
            .filter(ServiceBooking.vehicle_id == vehicle_id)
            .order_by(ServiceBooking.service_date.desc())
            .all()
        )
