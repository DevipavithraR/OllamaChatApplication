from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Doctor import Doctor
from app.models.Department import Department
from app.repositories.DoctorRepository import DoctorRepository
from app.repositories.DepartmentRepository import DepartmentRepository
from app.schemas.doctor_schema import DoctorCreate, DoctorUpdate
from fastapi import HTTPException, status

class DoctorSearchService:
    def __init__(self, db: Session):
        self.doctor_repo = DoctorRepository(db)
        self.dept_repo = DepartmentRepository(db)

    def create_doctor(self, doctor_in: DoctorCreate) -> Doctor:
        """
        Create a new doctor.
        """
        doctor = Doctor(
            name=doctor_in.name,
            department=doctor_in.department,
            specialization=doctor_in.specialization,
            experience=doctor_in.experience,
            consultation_fee=doctor_in.consultation_fee,
            available_days=doctor_in.available_days,
            available_time=doctor_in.available_time,
            status=doctor_in.status
        )
        return self.doctor_repo.create(doctor)

    def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        """
        Get doctor by ID.
        """
        doctor = self.doctor_repo.get(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with ID {doctor_id} not found."
            )
        return doctor

    def get_doctor_by_name(self, name: str) -> Optional[Doctor]:
        """
        Get doctor by name.
        """
        return self.doctor_repo.get_by_name(name)

    def get_all_doctors(self, skip: int = 0, limit: int = 100) -> List[Doctor]:
        """
        Get all doctors with pagination.
        """
        return self.doctor_repo.get_all(skip, limit)

    def get_active_doctors(self) -> List[Doctor]:
        """
        Get all active doctors.
        """
        return self.doctor_repo.get_active_doctors()

    def search_doctors(self, query: str) -> List[Doctor]:
        """
        Search doctors based on user input keywords (e.g. Cardiologist, Priya, Pediatrics).
        """
        # Split keywords to match Doctor name, specialization, or department
        keywords = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
        if query.strip() and query.strip().lower() not in keywords:
            keywords.append(query.strip().lower())
        
        # Strip common titles like 'dr' or 'dr.'
        cleaned_keywords = []
        for kw in keywords:
            clean = kw.replace("dr.", "").replace("dr", "").strip()
            if clean:
                cleaned_keywords.append(clean)
        
        return self.doctor_repo.search_by_keywords(cleaned_keywords)

    def update_doctor(self, doctor_id: int, doctor_in: DoctorUpdate) -> Doctor:
        """
        Update doctor details.
        """
        doctor = self.get_doctor_by_id(doctor_id)
        update_data = doctor_in.model_dump(exclude_unset=True)
        return self.doctor_repo.update(doctor, update_data)

    def delete_doctor(self, doctor_id: int) -> Doctor:
        """
        Delete a doctor.
        """
        doctor = self.get_doctor_by_id(doctor_id)
        self.doctor_repo.delete(doctor_id)
        return doctor

    # Department methods
    def get_all_departments(self) -> List[Department]:
        """
        Get all departments.
        """
        return self.dept_repo.get_all(limit=100)

    def get_department_by_name(self, name: str) -> Optional[Department]:
        """
        Get department by name.
        """
        return self.dept_repo.get_by_name(name)
