import logging
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.models.Admission import Admission
from app.models.Student import Student
from app.models.Course import Course
from app.repositories.AdmissionRepository import AdmissionRepository
from app.repositories.StudentRepository import StudentRepository
from app.repositories.CourseRepository import CourseRepository
from app.schemas.admission_schema import AdmissionCreate, AdmissionCreateWithStudent
from fastapi import HTTPException, status

logger = logging.getLogger("app.services.AdmissionService")

class AdmissionService:
    def __init__(self, db: Session):
        self.db = db
        self.admission_repo = AdmissionRepository(db)
        self.student_repo = StudentRepository(db)
        self.course_repo = CourseRepository(db)

    def create_admission(self, dto: AdmissionCreate) -> Admission:
        """
        Creates an admission application for an existing student and course.
        Decrements the course's available seat count by 1.
        """
        student = self.student_repo.get(dto.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {dto.student_id} not found."
            )
        course = self.course_repo.get(dto.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {dto.course_id} not found."
            )
        if course.available_seats <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No seats available in {course.course_name}."
            )
        
        admission = Admission(
            student_id=dto.student_id,
            course_id=dto.course_id,
            application_date=dto.application_date,
            status=dto.status or "Pending Verification",
            remarks=dto.remarks or f"Applied for course: {course.course_name}"
        )
        
        course.available_seats -= 1
        
        self.admission_repo.create(admission)
        self.db.commit()
        self.db.refresh(admission)
        return admission

    def create_admission_with_student(self, dto: AdmissionCreateWithStudent) -> Admission:
        """
        Orchestrates student profile setup / lookup and registers their admission application.
        Decrements the course's available seat count by 1.
        """
        # 1. Resolve student profile
        student = self.student_repo.get_by_phone_number(dto.student_phone)
        if not student:
            logger.info(f"Registering new student: {dto.student_name} ({dto.student_phone})")
            student = Student(
                name=dto.student_name,
                phone_number=dto.student_phone,
                email=dto.student_email,
                date_of_birth=dto.student_dob,
                gender=dto.student_gender,
                address=dto.student_address,
                marks_percentage=dto.marks_percentage
            )
            student = self.student_repo.create(student)
        else:
            # Update email/marks/details if provided and missing
            updated = False
            if dto.student_email and not student.email:
                student.email = dto.student_email
                updated = True
            if dto.marks_percentage is not None and not student.marks_percentage:
                student.marks_percentage = dto.marks_percentage
                updated = True
            if dto.student_gender and not student.gender:
                student.gender = dto.student_gender
                updated = True
            if dto.student_address and not student.address:
                student.address = dto.student_address
                updated = True
            if dto.student_dob and not student.date_of_birth:
                student.date_of_birth = dto.student_dob
                updated = True
            if updated:
                self.db.commit()
                self.db.refresh(student)

        # 2. Resolve course
        course = self.course_repo.get_by_name_exact(dto.course_name)
        if not course:
            # Fallback search by substring
            courses = self.course_repo.search_by_name(dto.course_name)
            if courses:
                course = courses[0]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course '{dto.course_name}' is not offered by our college."
                )

        # 3. Check seat availability
        if course.available_seats <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No seats available in {course.course_name}."
            )

        # 4. Create admission record
        admission = Admission(
            student_id=student.student_id,
            course_id=course.course_id,
            application_date=dto.application_date,
            status="Pending Verification",
            remarks=dto.remarks or f"Applied with marks: {student.marks_percentage}%"
        )
        
        # Decrement available seats
        course.available_seats -= 1
        
        # Save records
        self.admission_repo.create(admission)
        self.db.commit()
        self.db.refresh(admission)
        
        logger.info(f"Admission application {admission.admission_id} created. Seat count updated.")
        return admission

    def get_admission_by_id(self, id: int) -> Admission:
        admission = self.admission_repo.get(id)
        if not admission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Admission Application #{id} not found."
            )
        return admission

    def get_all_admissions(self, skip: int = 0, limit: int = 100) -> List[Admission]:
        return self.admission_repo.get_all(skip, limit)

    def cancel_admission(self, id: int) -> Admission:
        """
        Cancels an admission and restores the seat back to the course.
        """
        admission = self.get_admission_by_id(id)
        if admission.status == "Cancelled":
            return admission

        admission.status = "Cancelled"
        
        # Restore available seats
        if admission.course:
            admission.course.available_seats += 1
            
        self.db.commit()
        self.db.refresh(admission)
        logger.info(f"Admission application {id} marked as Cancelled. Seat returned.")
        return admission

    def update_admission_status(self, id: int, status_str: str, remarks: str = None) -> Admission:
        admission = self.get_admission_by_id(id)
        
        # If transitioning from active to Cancelled
        if status_str == "Cancelled" and admission.status != "Cancelled":
            if admission.course:
                admission.course.available_seats += 1
        # If transitioning from Cancelled to active
        elif status_str != "Cancelled" and admission.status == "Cancelled":
            if admission.course:
                if admission.course.available_seats <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot restore admission; no available seats in the course."
                    )
                admission.course.available_seats -= 1

        admission.status = status_str
        if remarks:
            admission.remarks = remarks
            
        self.db.commit()
        self.db.refresh(admission)
        return admission

    def get_active_admissions(self, student_id: int) -> List[Admission]:
        return self.admission_repo.get_active_by_student_id(student_id)
