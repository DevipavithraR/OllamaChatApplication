from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.booking_schema import BookingCreate, BookingCreateWithCustomer, BookingUpdate, BookingResponse
from app.services.BookingService import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.create_booking(booking)

@router.post("/customer", response_model=BookingResponse)
def create_booking_with_customer(booking: BookingCreateWithCustomer, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.create_booking_with_customer(booking)

@router.get("", response_model=List[BookingResponse])
def get_all_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_all_bookings(skip, limit)

@router.get("/customer/{customer_id}", response_model=List[BookingResponse])
def get_bookings_by_customer(customer_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_bookings_by_customer(customer_id)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_booking_by_id(booking_id)

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.update_booking(booking_id, booking)

@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.cancel_booking(booking_id)

@router.delete("/{booking_id}", response_model=BookingResponse)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.delete_booking(booking_id)
