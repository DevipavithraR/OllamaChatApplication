import json
import re
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.PatientService import PatientService
from app.services.AppointmentService import AppointmentService
from app.repositories.ConversationRepository import ConversationRepository
from app.schemas.patient_schema import PatientCreate
from app.schemas.appointment_schema import AppointmentCreateWithPatient

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.patient_service = PatientService(db)
        self.appointment_service = AppointmentService(db)
        self.conversation_repo = ConversationRepository(db)

    def intercept_and_execute(self, conversation_id: int, response_text: str) -> str:
        """
        Scans LLM output for action tags (PATIENT_IDENTIFY, APPOINTMENT_CONFIRM, 
        APPOINTMENT_CANCEL, APPOINTMENT_RESCHEDULE).
        Parses the JSON payloads, updates the DB, and strips tags from the response.
        """
        cleaned_text = response_text

        # 1. Intercept PATIENT_IDENTIFY
        patient_pattern = r"```PATIENT_IDENTIFY\s*(\{.*?\})\s*```"
        patient_match = re.search(patient_pattern, response_text, re.DOTALL)
        if patient_match:
            json_str = patient_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing patient identification action: {data}")
                
                phone = data["phone"]
                name = data["name"]
                
                # Check if patient exists, else create
                patient = self.patient_service.get_patient_by_phone(phone)
                if not patient:
                    patient = self.patient_service.create_patient(
                        PatientCreate(name=name, phone_number=phone)
                    )
                
                # Link conversation to patient
                self.conversation_repo.link_patient(conversation_id, patient.patient_id)
                logger.info(f"Linked conversation {conversation_id} to patient {patient.patient_id}")
            except Exception as e:
                logger.error(f"Failed to process PATIENT_IDENTIFY block: {str(e)}")
            
            # Strip block from text
            cleaned_text = re.sub(patient_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. Intercept APPOINTMENT_CONFIRM
        confirm_pattern = r"```APPOINTMENT_CONFIRM\s*(\{.*?\})\s*```"
        confirm_match = re.search(confirm_pattern, response_text, re.DOTALL)
        if confirm_match:
            json_str = confirm_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing appointment confirm action: {data}")
                
                # Parse datetime string
                dt_str = data["appointment_datetime"]
                app_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                
                dto = AppointmentCreateWithPatient(
                    patient_name=data["name"],
                    patient_phone=data["phone"],
                    patient_email=data.get("email"),
                    patient_gender=data.get("gender"),
                    patient_age=data.get("age"),
                    doctor_name=data["doctor"],
                    department=data.get("department"),
                    appointment_datetime=app_time,
                    special_notes=data.get("special_notes"),
                    status="CONFIRMED"
                )
                
                appointment = self.appointment_service.create_appointment_with_patient(dto)
                # Link conversation to patient
                self.conversation_repo.link_patient(conversation_id, appointment.patient_id)
                logger.info(f"Successfully confirmed appointment {appointment.appointment_id} for patient {appointment.patient_id}")
            except Exception as e:
                logger.error(f"Failed to process APPOINTMENT_CONFIRM block: {str(e)}")
            
            cleaned_text = re.sub(confirm_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. Intercept APPOINTMENT_CANCEL
        cancel_pattern = r"```APPOINTMENT_CANCEL\s*(\{.*?\})\s*```"
        cancel_match = re.search(cancel_pattern, response_text, re.DOTALL)
        if cancel_match:
            json_str = cancel_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing appointment cancel action: {data}")
                
                app_id = int(data["appointment_id"])
                appointment = self.appointment_service.cancel_appointment(app_id)
                logger.info(f"Successfully cancelled appointment {appointment.appointment_id}")
            except Exception as e:
                logger.error(f"Failed to process APPOINTMENT_CANCEL block: {str(e)}")
            
            cleaned_text = re.sub(cancel_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. Intercept APPOINTMENT_RESCHEDULE
        resched_pattern = r"```APPOINTMENT_RESCHEDULE\s*(\{.*?\})\s*```"
        resched_match = re.search(resched_pattern, response_text, re.DOTALL)
        if resched_match:
            json_str = resched_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing appointment reschedule action: {data}")
                
                app_id = int(data["appointment_id"])
                dt_str = data["appointment_datetime"]
                new_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                
                appointment = self.appointment_service.reschedule_appointment(app_id, new_time)
                logger.info(f"Successfully rescheduled appointment {appointment.appointment_id} to {new_time}")
            except Exception as e:
                logger.error(f"Failed to process APPOINTMENT_RESCHEDULE block: {str(e)}")
            
            cleaned_text = re.sub(resched_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text
