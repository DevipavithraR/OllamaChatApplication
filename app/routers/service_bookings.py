from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.service_booking_schema import ServiceBookingCreate, ServiceBookingUpdate, ServiceBookingResponse
from app.services.BookingService import BookingService

router = APIRouter(prefix="/service_bookings", tags=["Service Bookings"])

@router.post("/", response_model=ServiceBookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: ServiceBookingCreate, db: Session = Depends(get_db)):
    """
    Schedule a new service booking.
    """
    service = BookingService(db)
    return service.create_booking(booking_in)

@router.get("/", response_model=List[ServiceBookingResponse])
def get_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all service bookings (paginated).
    """
    service = BookingService(db)
    return service.get_all_bookings(skip, limit)

@router.get("/{booking_id}", response_model=ServiceBookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a service booking by ID.
    """
    service = BookingService(db)
    return service.get_booking_by_id(booking_id)

@router.get("/customer/{phone}", response_model=List[ServiceBookingResponse])
def get_bookings_by_customer_phone(phone: str, db: Session = Depends(get_db)):
    """
    Retrieve all service bookings for a customer by phone number.
    """
    service = BookingService(db)
    return service.get_bookings_by_customer_phone(phone)

@router.put("/{booking_id}", response_model=ServiceBookingResponse)
def update_booking(booking_id: int, booking_in: ServiceBookingUpdate, db: Session = Depends(get_db)):
    """
    Update a service booking.
    """
    service = BookingService(db)
    return service.update_booking(booking_id, booking_in)

@router.delete("/{booking_id}", response_model=ServiceBookingResponse)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Remove or cancel a service booking.
    """
    service = BookingService(db)
    return service.delete_booking(booking_id)
