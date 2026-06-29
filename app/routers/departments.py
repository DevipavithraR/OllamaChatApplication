from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.services.CourseSearchService import CourseSearchService
from app.repositories.DepartmentRepository import DepartmentRepository
from app.models.Department import Department

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(dept_in: DepartmentCreate, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    existing = repo.get_by_name(dept_in.department_name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department '{dept_in.department_name}' already exists."
        )
    dept = Department(
        department_name=dept_in.department_name,
        description=dept_in.description,
        head_of_department=dept_in.head_of_department
    )
    return repo.create(dept)

@router.get("/", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    service = CourseSearchService(db)
    return service.get_all_departments()

@router.get("/{name}", response_model=DepartmentResponse)
def get_department(name: str, db: Session = Depends(get_db)):
    service = CourseSearchService(db)
    return service.get_department_by_name(name)
