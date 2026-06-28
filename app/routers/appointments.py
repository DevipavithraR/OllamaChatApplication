from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.services.AppointmentService import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment_in: AppointmentCreate, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.create_appointment(appointment_in)

@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.get_all_appointments(skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.get_appointment_by_id(appointment_id)

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, appointment_in: AppointmentUpdate, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.update_appointment(appointment_id, appointment_in)

@router.delete("/{appointment_id}", response_model=AppointmentResponse)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.delete_appointment(appointment_id)
