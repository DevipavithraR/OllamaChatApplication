import logging
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories.ConversationRepository import ConversationRepository
from app.repositories.MessageRepository import MessageRepository
from app.services.StudentService import StudentService
from app.services.CourseSearchService import CourseSearchService
from app.services.AdmissionService import AdmissionService
from app.services.OllamaService import OllamaService
from app.services.PromptBuilder import PromptBuilder
from app.services.ActionInterceptor import ActionInterceptor

logger = logging.getLogger("app.services.ChatService")

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.student_service = StudentService(db)
        self.course_service = CourseSearchService(db)
        self.admission_service = AdmissionService(db)
        self.ollama_service = OllamaService()
        self.action_interceptor = ActionInterceptor(db)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Main chat orchestration method:
        1. Fetch/Create Conversation by session_id.
        2. Perform RAG query on Courses/Departments.
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

        # 2. RAG: Search courses based on user message keywords
        courses = self.course_service.search_courses(user_message)
        
        # If no specific matches but user asks about courses, duration, fees, eligibility, seats
        if not courses and any(word in user_message.lower() for word in ["course", "duration", "fee", "fees", "eligibility", "seat", "seats", "admission", "register", "apply"]):
            courses = self.course_service.get_all_courses()[:6]

        course_context = ""
        if courses:
            course_context = "\n".join([
                f"- Course: {c.course_name} (Duration: {c.duration}, Fees: ₹{c.fees} per year, Eligibility: {c.eligibility}, Available Seats: {c.available_seats}/{c.total_seats}). Description: {c.description or 'N/A'}"
                for c in courses
            ])
        else:
            course_context = "No specific courses matched in the search. We offer courses like B.Tech Computer Science, B.Tech Data Science, B.Tech Electronics & Comm., and M.Tech Software Engineering."

        # RAG: Search departments
        departments = self.course_service.get_all_departments()
        matching_depts = []
        for dept in departments:
            if dept.department_name.lower() in user_message.lower() or (dept.description and dept.description.lower() in user_message.lower()):
                matching_depts.append(dept)
        
        # If no specific match, list first few departments
        if not matching_depts and any(word in user_message.lower() for word in ["department", "dept", "computer science", "electronics", "information technology", "mechanical"]):
            matching_depts = departments[:4]

        department_context = ""
        if matching_depts:
            department_context = "\n".join([
                f"- {dept.department_name} (Head of Department: {dept.head_of_department or 'N/A'}): {dept.description}"
                for dept in matching_depts
            ])
        else:
            department_context = "Departments: Computer Science, Electronics & Communication, Information Technology, and Mechanical Engineering are available."

        # RAG: Student profile context
        student_context = "Anonymous Student"
        active_admissions_context = "No previous applications found."

        if conversation.student_id:
            try:
                student = self.student_service.get_student_by_id(conversation.student_id)
                student_context = f"Identified Student: {student.name} (Phone: {student.phone_number}, Email: {student.email or 'N/A'}, DOB: {student.date_of_birth or 'N/A'}, Gender: {student.gender or 'N/A'}, Marks: {student.marks_percentage or 'N/A'}%)"
                
                # Retrieve student admissions
                admissions = self.admission_service.get_active_admissions(student.student_id)
                if admissions:
                    active_admissions_context = "\n".join([
                        f"- Application ID #{adm.admission_id}: for {adm.course.course_name} on {adm.application_date.strftime('%Y-%m-%d')} [Status: {adm.status}]"
                        for adm in admissions
                    ])
                else:
                    active_admissions_context = "No active applications found for this student."
            except Exception as e:
                logger.error(f"Error fetching student or admission contexts: {str(e)}")

        # 3. Build dynamic system prompt
        system_prompt = PromptBuilder.build_system_prompt(
            course_context=course_context,
            department_context=department_context,
            student_context=student_context,
            active_applications_context=active_admissions_context,
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

        # Reload conversation to check if student_id was linked during action interception
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "student_id": conversation.student_id
        }
