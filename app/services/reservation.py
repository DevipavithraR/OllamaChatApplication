from typing import List
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.repositories.reservation import ReservationRepository
from app.services.customer import CustomerService
from app.schemas.customer import CustomerCreate
from app.schemas.reservation import ReservationCreate, ReservationCreateWithCustomer, ReservationUpdate
from fastapi import HTTPException, status

class ReservationService:
    def __init__(self, db: Session):
        self.repository = ReservationRepository(db)
        self.customer_service = CustomerService(db)

    def create_reservation(self, reservation_in: ReservationCreate) -> Reservation:
        """
        Create a reservation for an existing customer ID.
        """
        # Ensure customer exists
        self.customer_service.get_customer_by_id(reservation_in.customer_id)
        
        reservation = Reservation(
            customer_id=reservation_in.customer_id,
            reservation_time=reservation_in.reservation_time,
            party_size=reservation_in.party_size,
            special_requests=reservation_in.special_requests,
            status=reservation_in.status
        )
        return self.repository.create(reservation)

    def create_reservation_with_customer(self, reservation_in: ReservationCreateWithCustomer) -> Reservation:
        """
        Create a reservation by providing customer details directly.
        Will find the customer by phone or create a new customer if not found.
        """
        customer = self.customer_service.get_customer_by_phone(reservation_in.customer_phone)
        if not customer:
            customer_create = CustomerCreate(
                name=reservation_in.customer_name,
                phone=reservation_in.customer_phone,
                email=reservation_in.customer_email
            )
            customer = self.customer_service.create_customer(customer_create)

        reservation = Reservation(
            customer_id=customer.id,
            reservation_time=reservation_in.reservation_time,
            party_size=reservation_in.party_size,
            special_requests=reservation_in.special_requests,
            status=reservation_in.status
        )
        return self.repository.create(reservation)

    def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        """
        Get a reservation by ID.
        """
        reservation = self.repository.get(reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reservation with ID {reservation_id} not found."
            )
        return reservation

    def get_reservations_by_customer_phone(self, phone: str) -> List[Reservation]:
        """
        Retrieve all reservations for a customer looked up by phone.
        """
        return self.repository.get_by_customer_phone(phone)

    def get_all_reservations(self, skip: int = 0, limit: int = 100) -> List[Reservation]:
        """
        Retrieve a paginated list of reservations.
        """
        return self.repository.get_all(skip, limit)

    def update_reservation(self, reservation_id: int, reservation_in: ReservationUpdate) -> Reservation:
        """
        Update reservation details.
        """
        reservation = self.get_reservation_by_id(reservation_id)
        update_data = reservation_in.model_dump(exclude_unset=True)
        return self.repository.update(reservation, update_data)

    def delete_reservation(self, reservation_id: int) -> Reservation:
        """
        Delete a reservation.
        """
        reservation = self.get_reservation_by_id(reservation_id)
        return self.repository.delete(reservation_id)
