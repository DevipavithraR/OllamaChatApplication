from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trainer_booking_schema import TrainerBookingCreate, TrainerBookingUpdate, TrainerBookingResponse
from app.services.TrainerSearchService import TrainerSearchService

router = APIRouter(prefix="/trainer_bookings", tags=["Trainer Bookings"])

@router.post("/", response_model=TrainerBookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: TrainerBookingCreate, db: Session = Depends(get_db)):
    """
    Book a session with a trainer.
    """
    service = TrainerSearchService(db)
    return service.create_booking(booking_in)

@router.get("/", response_model=List[TrainerBookingResponse])
def get_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all trainer bookings.
    """
    service = TrainerSearchService(db)
    return service.get_all_bookings(skip, limit)

@router.get("/member/{phone}", response_model=List[TrainerBookingResponse])
def get_bookings_by_member_phone(phone: str, db: Session = Depends(get_db)):
    """
    Retrieve trainer bookings by member phone number.
    """
    service = TrainerSearchService(db)
    return service.booking_repository.get_bookings_by_member_phone(phone)

@router.get("/{booking_id}", response_model=TrainerBookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a booking by ID.
    """
    service = TrainerSearchService(db)
    return service.get_booking_by_id(booking_id)

@router.put("/{booking_id}", response_model=TrainerBookingResponse)
def update_booking(booking_id: int, booking_in: TrainerBookingUpdate, db: Session = Depends(get_db)):
    """
    Update booking details.
    """
    service = TrainerSearchService(db)
    return service.update_booking(booking_id, booking_in)

@router.delete("/{booking_id}", response_model=TrainerBookingResponse)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Cancel/delete a booking.
    """
    service = TrainerSearchService(db)
    # The prompt cancellation specifies to cancel the booking (status update to CANCELLED) or delete it.
    # In reservation.py, it deleted it: self.repository.delete(id)
    # Let's delete it so the record matches the old reservation deletion behavior, or set status to CANCELLED.
    # Actually, in reservation, delete_reservation returned the deleted object. Let's delete the booking.
    return service.delete_booking(booking_id)
