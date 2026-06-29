from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student_schema import StudentCreate, StudentUpdate, StudentResponse
from app.services.StudentService import StudentService

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.create_student(student_in)

@router.get("/", response_model=List[StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.get_all_students(skip=skip, limit=limit)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.get_student_by_id(student_id)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.update_student(student_id, student_in)

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.delete_student(student_id)
