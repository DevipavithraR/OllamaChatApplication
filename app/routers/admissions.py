from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admission_schema import AdmissionCreate, AdmissionUpdate, AdmissionResponse
from app.services.AdmissionService import AdmissionService

router = APIRouter(prefix="/admissions", tags=["Admissions"])

@router.post("/", response_model=AdmissionResponse, status_code=status.HTTP_201_CREATED)
def create_admission(admission_in: AdmissionCreate, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.create_admission(admission_in)

@router.get("/", response_model=List[AdmissionResponse])
def get_admissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.get_all_admissions(skip=skip, limit=limit)

@router.get("/{admission_id}", response_model=AdmissionResponse)
def get_admission(admission_id: int, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.get_admission_by_id(admission_id)

@router.put("/{admission_id}", response_model=AdmissionResponse)
def update_admission(admission_id: int, admission_in: AdmissionUpdate, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.update_admission_status(
        admission_id, 
        admission_in.status, 
        admission_in.remarks
    )

@router.delete("/{admission_id}", response_model=AdmissionResponse)
def delete_admission(admission_id: int, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.cancel_admission(admission_id)
