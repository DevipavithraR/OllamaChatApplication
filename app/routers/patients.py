from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientResponse
from app.services.PatientService import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.create_patient(patient_in)

@router.get("/", response_model=List[PatientResponse])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.get_all_patients(skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.get_patient_by_id(patient_id)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_in: PatientUpdate, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.update_patient(patient_id, patient_in)

@router.delete("/{patient_id}", response_model=PatientResponse)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.delete_patient(patient_id)
