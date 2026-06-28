from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Patient import Patient
from app.repositories.PatientRepository import PatientRepository
from app.schemas.patient_schema import PatientCreate, PatientUpdate
from fastapi import HTTPException, status

class PatientService:
    def __init__(self, db: Session):
        self.repository = PatientRepository(db)

    def create_patient(self, patient_in: PatientCreate) -> Patient:
        """
        Create a new patient. Raises HTTP 400 if patient already exists by phone.
        """
        existing = self.repository.get_by_phone_number(patient_in.phone_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Patient with phone number '{patient_in.phone_number}' already exists."
            )

        patient = Patient(
            name=patient_in.name,
            phone_number=patient_in.phone_number,
            email=patient_in.email,
            gender=patient_in.gender,
            age=patient_in.age
        )
        return self.repository.create(patient)

    def get_patient_by_id(self, patient_id: int) -> Patient:
        """
        Retrieve a patient by ID.
        """
        patient = self.repository.get(patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with ID {patient_id} not found."
            )
        return patient

    def get_patient_by_phone(self, phone: str) -> Optional[Patient]:
        """
        Retrieve patient by phone.
        """
        return self.repository.get_by_phone_number(phone)

    def get_all_patients(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """
        Retrieve all patients with pagination.
        """
        return self.repository.get_all(skip, limit)

    def update_patient(self, patient_id: int, patient_in: PatientUpdate) -> Patient:
        """
        Update an existing patient.
        """
        patient = self.get_patient_by_id(patient_id)
        update_data = patient_in.model_dump(exclude_unset=True)
        
        if "phone_number" in update_data and update_data["phone_number"] != patient.phone_number:
            existing = self.repository.get_by_phone_number(update_data["phone_number"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Patient with phone number '{update_data['phone_number']}' already exists."
                )

        return self.repository.update(patient, update_data)

    def delete_patient(self, patient_id: int) -> Patient:
        """
        Delete a patient.
        """
        patient = self.get_patient_by_id(patient_id)
        self.repository.delete(patient_id)
        return patient
