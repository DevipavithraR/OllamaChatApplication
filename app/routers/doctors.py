from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.doctor_schema import DoctorCreate, DoctorUpdate, DoctorResponse
from app.services.DoctorSearchService import DoctorSearchService

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.create_doctor(doctor_in)

@router.get("/", response_model=List[DoctorResponse])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.get_all_doctors(skip=skip, limit=limit)

@router.get("/search", response_model=List[DoctorResponse])
def search_doctors(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.search_doctors(q)

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.get_doctor_by_id(doctor_id)

@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_in: DoctorUpdate, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.update_doctor(doctor_id, doctor_in)

@router.delete("/{doctor_id}", response_model=DoctorResponse)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.delete_doctor(doctor_id)
