from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.Appointment import Appointment
from app.repositories.BaseRepository import BaseRepository

class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, db: Session):
        super().__init__(Appointment, db)

    def get_upcoming_appointments_for_patient(self, patient_id: int) -> List[Appointment]:
        """
        Retrieve all active upcoming appointments for a patient.
        """
        return (
            self.db.query(Appointment)
            .filter(Appointment.patient_id == patient_id)
            .filter(Appointment.appointment_datetime >= datetime.utcnow())
            .filter(Appointment.status != "CANCELLED")
            .all()
        )
