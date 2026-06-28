import logging
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories.ConversationRepository import ConversationRepository
from app.repositories.MessageRepository import MessageRepository
from app.services.PatientService import PatientService
from app.services.DoctorSearchService import DoctorSearchService
from app.services.AppointmentService import AppointmentService
from app.services.OllamaService import OllamaService
from app.services.PromptBuilder import PromptBuilder
from app.services.ActionInterceptor import ActionInterceptor

logger = logging.getLogger("app.services.ChatService")

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.patient_service = PatientService(db)
        self.doctor_service = DoctorSearchService(db)
        self.appointment_service = AppointmentService(db)
        self.ollama_service = OllamaService()
        self.action_interceptor = ActionInterceptor(db)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Main chat orchestration method:
        1. Fetch/Create Conversation by session_id.
        2. Perform RAG query on Doctors/Departments.
        3. Build system prompt context.
        4. Query Ollama with prompt + message history + user message.
        5. Intercept action tags and execute database modifications.
        6. Persist user and bot messages.
        7. Return response payload.
        """
        # 1. Fetch or create conversation
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            from app.models.Conversation import Conversation
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)

        # Retrieve last 10 messages for history
        history_messages = self.message_repo.get_last_n_messages(conversation.conversation_id, limit=10)

        # 2. RAG: Search doctors based on user message keywords
        doctors = self.doctor_service.search_doctors(user_message)
        
        # If no specific matches but user asks about doctors/specialists/departments, fetch some default doctors
        if not doctors and any(word in user_message.lower() for word in ["doctor", "specialist", "md", "physician", "appointment", "schedule", "book", "fee", "timing"]):
            doctors = self.doctor_service.get_active_doctors()[:8]

        doctor_context = ""
        if doctors:
            doctor_context = "\n".join([
                f"- {doc.name} ({doc.specialization} at {doc.department} Department): Experience: {doc.experience} Years. Consultation Fee: ₹{doc.consultation_fee}. Available Days: {doc.available_days}, Available Time: {doc.available_time}."
                for doc in doctors
            ])
        else:
            doctor_context = "No specific doctors matched. Assure the patient that we have premium doctors in all major departments."

        # RAG: Search departments based on user message keywords
        departments = self.doctor_service.get_all_departments()
        matching_depts = []
        for dept in departments:
            if dept.department_name.lower() in user_message.lower() or dept.description.lower() in user_message.lower():
                matching_depts.append(dept)
        
        # If no specific match, list first few departments
        if not matching_depts and any(word in user_message.lower() for word in ["department", "clinic", "ward", "cardio", "pedi", "ortho", "neuro"]):
            matching_depts = departments[:5]

        department_context = ""
        if matching_depts:
            department_context = "\n".join([
                f"- {dept.department_name} Department: {dept.description}"
                for dept in matching_depts
            ])
        else:
            department_context = "Departments: Cardiology, Pediatrics, Orthopedics, Neurology, General Medicine are available."

        # RAG: Patient profile context
        patient_context = "Anonymous Patient"
        upcoming_appointments_context = "No upcoming appointments found."

        if conversation.patient_id:
            try:
                patient = self.patient_service.get_patient_by_id(conversation.patient_id)
                patient_context = f"Identified Patient: {patient.name} (Phone: {patient.phone_number}, Email: {patient.email or 'N/A'}, Age: {patient.age or 'N/A'}, Gender: {patient.gender or 'N/A'})"
                
                # Retrieve upcoming appointments
                appointments = self.appointment_service.get_upcoming_appointments(patient.patient_id)
                if appointments:
                    upcoming_appointments_context = "\n".join([
                        f"- Appointment ID {app.appointment_id}: with {app.doctor.name} ({app.doctor.specialization}) on {app.appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')} [Status: {app.status}]"
                        for app in appointments
                    ])
                else:
                    upcoming_appointments_context = "No upcoming appointments found for this patient."
            except Exception as e:
                logger.error(f"Error fetching patient or appointment contexts: {str(e)}")

        # 3. Build dynamic system prompt
        system_prompt = PromptBuilder.build_system_prompt(
            doctor_context=doctor_context,
            department_context=department_context,
            patient_context=patient_context,
            upcoming_appointments_context=upcoming_appointments_context,
            current_time=datetime.now()
        )

        # 4. Prepare message list for Ollama
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            ollama_messages.append({
                "role": "user" if msg.sender == "user" else "assistant", 
                "content": msg.message
            })
        ollama_messages.append({"role": "user", "content": user_message})

        # Save user message to database
        self.message_repo.add_message(conversation.conversation_id, sender="user", message=user_message)

        # 5. Call Ollama model
        bot_response = self.ollama_service.chat(ollama_messages)

        # 6. Intercept and execute structured action tags
        bot_response = self.action_interceptor.intercept_and_execute(conversation.conversation_id, bot_response)

        # Save bot response to database
        self.message_repo.add_message(conversation.conversation_id, sender="bot", message=bot_response)

        # Reload conversation to check if patient_id was linked during action interception
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "patient_id": conversation.patient_id
        }
