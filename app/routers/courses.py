from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.course_schema import CourseCreate, CourseUpdate, CourseResponse
from app.repositories.CourseRepository import CourseRepository
from app.models.Course import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    existing = repo.get_by_name_exact(course_in.course_name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course '{course_in.course_name}' already exists."
        )
    course = Course(
        course_name=course_in.course_name,
        department_id=course_in.department_id,
        duration=course_in.duration,
        total_seats=course_in.total_seats,
        available_seats=course_in.available_seats,
        fees=course_in.fees,
        eligibility=course_in.eligibility,
        description=course_in.description
    )
    return repo.create(course)

@router.get("/", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    return repo.get_all(skip, limit)

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    course = repo.get(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_in: CourseUpdate, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    course = repo.get(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    update_data = course_in.model_dump(exclude_unset=True)
    return repo.update(course, update_data)

@router.delete("/{course_id}", response_model=CourseResponse)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    course = repo.get(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )
    repo.delete(course_id)
    return course
