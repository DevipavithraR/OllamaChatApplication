from app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientResponse
from app.schemas.doctor_schema import DoctorCreate, DoctorUpdate, DoctorResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.schemas.appointment_schema import (
    AppointmentCreate, 
    AppointmentCreateWithPatient, 
    AppointmentReschedule, 
    AppointmentUpdate, 
    AppointmentResponse
)
from app.schemas.conversation_schema import ChatRequest, ChatResponse, ConversationResponse
from app.schemas.message_schema import MessageResponse

__all__ = [
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "DoctorCreate",
    "DoctorUpdate",
    "DoctorResponse",
    "DepartmentCreate",
    "DepartmentResponse",
    "AppointmentCreate",
    "AppointmentCreateWithPatient",
    "AppointmentReschedule",
    "AppointmentUpdate",
    "AppointmentResponse",
    "ChatRequest",
    "ChatResponse",
    "ConversationResponse",
    "MessageResponse"
]
