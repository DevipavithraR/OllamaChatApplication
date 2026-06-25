from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.reservation import (
    ReservationCreate,
    ReservationCreateWithCustomer,
    ReservationUpdate,
    ReservationResponse
)
from app.services.reservation import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation_in: ReservationCreate, db: Session = Depends(get_db)):
    """
    Book a table using an existing Customer ID.
    """
    service = ReservationService(db)
    return service.create_reservation(reservation_in)

@router.post("/with-customer", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation_with_customer(
    reservation_in: ReservationCreateWithCustomer,
    db: Session = Depends(get_db)
):
    """
    Book a table by providing Customer name, phone, and optional email.
    If the customer does not exist, a new customer record will be automatically created.
    """
    service = ReservationService(db)
    return service.create_reservation_with_customer(reservation_in)

@router.get("/", response_model=List[ReservationResponse])
def get_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all reservations (paginated).
    """
    service = ReservationService(db)
    return service.get_all_reservations(skip, limit)

@router.get("/customer/{phone}", response_model=List[ReservationResponse])
def get_reservations_by_phone(phone: str, db: Session = Depends(get_db)):
    """
    Retrieve reservations using a customer's phone number.
    """
    service = ReservationService(db)
    return service.get_reservations_by_customer_phone(phone)

@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific reservation by ID.
    """
    service = ReservationService(db)
    return service.get_reservation_by_id(reservation_id)

@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_in: ReservationUpdate,
    db: Session = Depends(get_db)
):
    """
    Modify reservation details (time, party size, status, or requests).
    """
    service = ReservationService(db)
    return service.update_reservation(reservation_id, reservation_in)

@router.delete("/{reservation_id}", response_model=ReservationResponse)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Cancel and remove a reservation from the system.
    """
    service = ReservationService(db)
    return service.delete_reservation(reservation_id)
