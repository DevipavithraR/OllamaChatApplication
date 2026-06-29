from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Student import Student
from app.repositories.StudentRepository import StudentRepository
from app.schemas.student_schema import StudentCreate, StudentUpdate
from fastapi import HTTPException, status

class StudentService:
    def __init__(self, db: Session):
        self.repository = StudentRepository(db)

    def create_student(self, student_in: StudentCreate) -> Student:
        """
        Create a new student. Raises HTTP 400 if student already exists by phone.
        """
        existing = self.repository.get_by_phone_number(student_in.phone_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with phone number '{student_in.phone_number}' already exists."
            )

        student = Student(
            name=student_in.name,
            phone_number=student_in.phone_number,
            email=student_in.email,
            date_of_birth=student_in.date_of_birth,
            gender=student_in.gender,
            address=student_in.address,
            marks_percentage=student_in.marks_percentage
        )
        return self.repository.create(student)

    def get_student_by_id(self, student_id: int) -> Student:
        """
        Retrieve a student by ID.
        """
        student = self.repository.get(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found."
            )
        return student

    def get_student_by_phone(self, phone: str) -> Optional[Student]:
        """
        Retrieve student by phone.
        """
        return self.repository.get_by_phone_number(phone)

    def get_all_students(self, skip: int = 0, limit: int = 100) -> List[Student]:
        """
        Retrieve all students with pagination.
        """
        return self.repository.get_all(skip, limit)

    def update_student(self, student_id: int, student_in: StudentUpdate) -> Student:
        """
        Update an existing student.
        """
        student = self.get_student_by_id(student_id)
        update_data = student_in.model_dump(exclude_unset=True)
        
        if "phone_number" in update_data and update_data["phone_number"] != student.phone_number:
            existing = self.repository.get_by_phone_number(update_data["phone_number"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with phone number '{update_data['phone_number']}' already exists."
                )

        return self.repository.update(student, update_data)

    def delete_student(self, student_id: int) -> Student:
        """
        Delete a student.
        """
        student = self.get_student_by_id(student_id)
        self.repository.delete(student_id)
        return student
