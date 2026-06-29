from app.schemas.student_schema import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.course_schema import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.schemas.admission_schema import (
    AdmissionCreate, 
    AdmissionCreateWithStudent, 
    AdmissionUpdate, 
    AdmissionResponse
)
from app.schemas.conversation_schema import ChatRequest, ChatResponse, ConversationResponse
from app.schemas.message_schema import MessageResponse

__all__ = [
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "DepartmentCreate",
    "DepartmentResponse",
    "AdmissionCreate",
    "AdmissionCreateWithStudent",
    "AdmissionUpdate",
    "AdmissionResponse",
    "ChatRequest",
    "ChatResponse",
    "ConversationResponse",
    "MessageResponse"
]
