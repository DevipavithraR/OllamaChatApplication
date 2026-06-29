import json
import re
import logging
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.services.StudentService import StudentService
from app.services.AdmissionService import AdmissionService
from app.repositories.ConversationRepository import ConversationRepository
from app.schemas.student_schema import StudentCreate
from app.schemas.admission_schema import AdmissionCreateWithStudent

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.student_service = StudentService(db)
        self.admission_service = AdmissionService(db)
        self.conversation_repo = ConversationRepository(db)

    def intercept_and_execute(self, conversation_id: int, response_text: str) -> str:
        """
        Scans LLM output for action tags (STUDENT_IDENTIFY, ADMISSION_APPLY, 
        ADMISSION_STATUS, APPLICATION_CANCEL).
        Parses the JSON payloads, updates the DB, and strips tags from the response.
        """
        cleaned_text = response_text

        # 1. Intercept STUDENT_IDENTIFY
        student_pattern = r"```STUDENT_IDENTIFY\s*(\{.*?\})\s*```"
        student_match = re.search(student_pattern, response_text, re.DOTALL)
        if student_match:
            json_str = student_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing student identification action: {data}")
                
                phone = data["phone"]
                name = data["name"]
                
                # Check if student exists, else create
                student = self.student_service.get_student_by_phone(phone)
                if not student:
                    student = self.student_service.create_student(
                        StudentCreate(name=name, phone_number=phone)
                    )
                
                # Link conversation to student
                self.conversation_repo.link_student(conversation_id, student.student_id)
                logger.info(f"Linked conversation {conversation_id} to student {student.student_id}")
            except Exception as e:
                logger.error(f"Failed to process STUDENT_IDENTIFY block: {str(e)}")
            
            # Strip block from text
            cleaned_text = re.sub(student_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. Intercept ADMISSION_APPLY
        apply_pattern = r"```ADMISSION_APPLY\s*(\{.*?\})\s*```"
        apply_match = re.search(apply_pattern, response_text, re.DOTALL)
        if apply_match:
            json_str = apply_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing admission apply action: {data}")
                
                # Parse date string
                date_str = data.get("application_date")
                app_date = date.today()
                if date_str:
                    try:
                        app_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                
                dto = AdmissionCreateWithStudent(
                    student_name=data["name"],
                    student_phone=data["phone"],
                    student_email=data.get("email"),
                    marks_percentage=float(data["marks_percentage"]) if data.get("marks_percentage") is not None else None,
                    course_name=data["course"],
                    application_date=app_date,
                    remarks=f"Applied via Chatbot interface on {app_date}"
                )
                
                admission = self.admission_service.create_admission_with_student(dto)
                # Link conversation to student
                self.conversation_repo.link_student(conversation_id, admission.student_id)
                logger.info(f"Successfully created admission {admission.admission_id} for student {admission.student_id}")
                
                # Append Application ID to bot response for user visibility
                app_id_info = f"\n\n**Application Submitted Successfully!** Your Application ID is **#{admission.admission_id}**."
                cleaned_text = cleaned_text + app_id_info
            except Exception as e:
                logger.error(f"Failed to process ADMISSION_APPLY block: {str(e)}")
                error_info = f"\n\n*Error: Could not process admission application: {str(e)}*"
                cleaned_text = cleaned_text + error_info
            
            cleaned_text = re.sub(apply_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. Intercept ADMISSION_STATUS
        status_pattern = r"```ADMISSION_STATUS\s*(\{.*?\})\s*```"
        status_match = re.search(status_pattern, response_text, re.DOTALL)
        if status_match:
            json_str = status_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing admission status action: {data}")
                
                app_id = int(data["application_id"])
                admission = self.admission_service.get_admission_by_id(app_id)
                
                status_info = f"\n\n**Application Status for #{app_id}:**\n- **Course:** {admission.course.course_name}\n- **Student Name:** {admission.student.name}\n- **Status:** {admission.status}\n- **Remarks:** {admission.remarks or 'N/A'}"
                cleaned_text = cleaned_text + status_info
            except Exception as e:
                logger.error(f"Failed to process ADMISSION_STATUS block: {str(e)}")
                error_info = f"\n\n*Error: Could not retrieve status: {str(e)}*"
                cleaned_text = cleaned_text + error_info
            
            cleaned_text = re.sub(status_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. Intercept APPLICATION_CANCEL
        cancel_pattern = r"```APPLICATION_CANCEL\s*(\{.*?\})\s*```"
        cancel_match = re.search(cancel_pattern, response_text, re.DOTALL)
        if cancel_match:
            json_str = cancel_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing application cancel action: {data}")
                
                app_id = int(data["application_id"])
                admission = self.admission_service.cancel_admission(app_id)
                logger.info(f"Successfully cancelled admission {admission.admission_id}")
                
                cancel_info = f"\n\n**Application #{app_id} has been cancelled successfully.**"
                cleaned_text = cleaned_text + cancel_info
            except Exception as e:
                logger.error(f"Failed to process APPLICATION_CANCEL block: {str(e)}")
                error_info = f"\n\n*Error: Could not cancel application: {str(e)}*"
                cleaned_text = cleaned_text + error_info
            
            cleaned_text = re.sub(cancel_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text
