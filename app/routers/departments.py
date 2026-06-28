from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.department_schema import DepartmentResponse
from app.services.DoctorSearchService import DoctorSearchService

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.get_all_departments()

@router.get("/{name}", response_model=DepartmentResponse)
def get_department(name: str, db: Session = Depends(get_db)):
    service = DoctorSearchService(db)
    return service.get_department_by_name(name)
