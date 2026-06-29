from typing import List
from sqlalchemy.orm import Session
from app.models.Booking import Booking
from app.models.customer import Customer
from app.repositories.BookingRepository import BookingRepository
from app.repositories.CustomerRepository import CustomerRepository
from app.repositories.ShowRepository import ShowRepository
from app.schemas.booking_schema import BookingCreate, BookingCreateWithCustomer, BookingUpdate
from fastapi import HTTPException, status

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.booking_repo = BookingRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.show_repo = ShowRepository(db)

    def create_booking(self, booking_in: BookingCreate) -> Booking:
        # Check show exists
        show = self.show_repo.get(booking_in.show_id)
        if not show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Show with ID {booking_in.show_id} not found."
            )

        # Check customer exists
        customer = self.customer_repo.get(booking_in.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {booking_in.customer_id} not found."
            )

        # Verify seats availability
        if show.available_seats < booking_in.number_of_tickets:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough seats available. Requested: {booking_in.number_of_tickets}, Available: {show.available_seats}"
            )

        # Update show available seats
        show.available_seats -= booking_in.number_of_tickets
        self.show_repo.update(show, {"available_seats": show.available_seats})

        # Seat numbers list to string
        seats_str = ", ".join(booking_in.seat_numbers)

        booking = Booking(
            customer_id=booking_in.customer_id,
            show_id=booking_in.show_id,
            seat_numbers=seats_str,
            number_of_tickets=booking_in.number_of_tickets,
            total_amount=booking_in.total_amount,
            booking_status=booking_in.booking_status or "Confirmed"
        )
        return self.booking_repo.create(booking)

    def create_booking_with_customer(self, booking_in: BookingCreateWithCustomer) -> Booking:
        # Find or create customer
        customer = self.customer_repo.get_by_phone_number(booking_in.phone)
        if not customer:
            customer = Customer(
                name=booking_in.name,
                phone_number=booking_in.phone,
                email=booking_in.email
            )
            customer = self.customer_repo.create(customer)

        show = self.show_repo.get(booking_in.show_id)
        if not show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Show with ID {booking_in.show_id} not found."
            )

        # Total amount calculation
        total_amount = float(show.ticket_price) * booking_in.number_of_tickets

        create_data = BookingCreate(
            customer_id=customer.customer_id,
            show_id=booking_in.show_id,
            seat_numbers=booking_in.seat_numbers,
            number_of_tickets=booking_in.number_of_tickets,
            total_amount=total_amount,
            booking_status="Confirmed"
        )
        return self.create_booking(create_data)

    def get_booking_by_id(self, booking_id: int) -> Booking:
        booking = self.booking_repo.get(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking with ID {booking_id} not found."
            )
        return booking

    def get_all_bookings(self, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.booking_repo.get_all(skip, limit)

    def get_bookings_by_customer(self, customer_id: int) -> List[Booking]:
        return self.booking_repo.get_by_customer_id(customer_id)

    def cancel_booking(self, booking_id: int) -> Booking:
        booking = self.get_booking_by_id(booking_id)
        if booking.booking_status == "Cancelled":
            return booking

        show = self.show_repo.get(booking.show_id)
        if show:
            show.available_seats += booking.number_of_tickets
            self.show_repo.update(show, {"available_seats": show.available_seats})

        booking = self.booking_repo.update(booking, {"booking_status": "Cancelled"})
        return booking

    def update_booking(self, booking_id: int, booking_update: BookingUpdate) -> Booking:
        booking = self.get_booking_by_id(booking_id)
        show = self.show_repo.get(booking.show_id)

        update_dict = booking_update.model_dump(exclude_unset=True)

        if "number_of_tickets" in update_dict and show:
            diff = update_dict["number_of_tickets"] - booking.number_of_tickets
            if diff != 0:
                if show.available_seats < diff:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Not enough seats available to modify booking. Required additional: {diff}, Available: {show.available_seats}"
                    )
                show.available_seats -= diff
                self.show_repo.update(show, {"available_seats": show.available_seats})
                
                # Recalculate amount if needed and not explicitly provided
                if "total_amount" not in update_dict:
                    update_dict["total_amount"] = float(show.ticket_price) * update_dict["number_of_tickets"]

        if "seat_numbers" in update_dict and update_dict["seat_numbers"] is not None:
            update_dict["seat_numbers"] = ", ".join(update_dict["seat_numbers"])

        return self.booking_repo.update(booking, update_dict)

    def delete_booking(self, booking_id: int) -> Booking:
        booking = self.get_booking_by_id(booking_id)
        if booking.booking_status != "Cancelled":
            show = self.show_repo.get(booking.show_id)
            if show:
                show.available_seats += booking.number_of_tickets
                self.show_repo.update(show, {"available_seats": show.available_seats})

        return self.booking_repo.delete(booking_id)
