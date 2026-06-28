from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.Appointment import Appointment
from app.repositories.AppointmentRepository import AppointmentRepository
from app.services.PatientService import PatientService
from app.services.DoctorSearchService import DoctorSearchService
from app.schemas.patient_schema import PatientCreate
from app.schemas.appointment_schema import AppointmentCreate, AppointmentCreateWithPatient, AppointmentUpdate
from fastapi import HTTPException, status

class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)
        self.patient_service = PatientService(db)
        self.doctor_service = DoctorSearchService(db)

    def create_appointment(self, appointment_in: AppointmentCreate) -> Appointment:
        """
        Create an appointment for an existing patient and doctor.
        """
        # Ensure patient and doctor exist
        self.patient_service.get_patient_by_id(appointment_in.patient_id)
        self.doctor_service.get_doctor_by_id(appointment_in.doctor_id)
        
        appointment = Appointment(
            patient_id=appointment_in.patient_id,
            doctor_id=appointment_in.doctor_id,
            appointment_datetime=appointment_in.appointment_datetime,
            status=appointment_in.status,
            special_notes=appointment_in.special_notes
        )
        return self.repository.create(appointment)

    def create_appointment_with_patient(self, appointment_in: AppointmentCreateWithPatient) -> Appointment:
        """
        Create an appointment by providing patient details directly.
        Will find the patient by phone or create a new patient if not found.
        """
        patient = self.patient_service.get_patient_by_phone(appointment_in.patient_phone)
        if not patient:
            patient_create = PatientCreate(
                name=appointment_in.patient_name,
                phone_number=appointment_in.patient_phone,
                email=appointment_in.patient_email,
                gender=appointment_in.patient_gender,
                age=appointment_in.patient_age
            )
            patient = self.patient_service.create_patient(patient_create)

        # Lookup doctor by name
        doctor = self.doctor_service.get_doctor_by_name(appointment_in.doctor_name)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with name '{appointment_in.doctor_name}' not found."
            )

        appointment = Appointment(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            appointment_datetime=appointment_in.appointment_datetime,
            status=appointment_in.status,
            special_notes=appointment_in.special_notes
        )
        return self.repository.create(appointment)

    def get_appointment_by_id(self, appointment_id: int) -> Appointment:
        """
        Get an appointment by ID.
        """
        appointment = self.repository.get(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found."
            )
        return appointment

    def get_upcoming_appointments(self, patient_id: int) -> List[Appointment]:
        """
        Retrieve all active upcoming appointments for a patient.
        """
        return self.repository.get_upcoming_appointments_for_patient(patient_id)

    def get_all_appointments(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """
        Retrieve a paginated list of appointments.
        """
        return self.repository.get_all(skip, limit)

    def update_appointment(self, appointment_id: int, appointment_in: AppointmentUpdate) -> Appointment:
        """
        Update appointment details.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        update_data = appointment_in.model_dump(exclude_unset=True)
        return self.repository.update(appointment, update_data)

    def cancel_appointment(self, appointment_id: int) -> Appointment:
        """
        Cancel an appointment by setting its status to CANCELLED.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        return self.repository.update(appointment, {"status": "CANCELLED"})

    def reschedule_appointment(self, appointment_id: int, new_datetime: datetime) -> Appointment:
        """
        Reschedule an appointment by changing its date/time and setting status to CONFIRMED or RESCHEDULED.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        return self.repository.update(appointment, {
            "appointment_datetime": new_datetime,
            "status": "RESCHEDULED"
        })

    def delete_appointment(self, appointment_id: int) -> Appointment:
        """
        Delete an appointment from database.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        return self.repository.delete(appointment_id)
