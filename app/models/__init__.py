from app.database import Base
from app.models.Student import Student
from app.models.Course import Course
from app.models.Department import Department
from app.models.Admission import Admission
from app.models.Conversation import Conversation
from app.models.Message import Message

__all__ = ["Base", "Student", "Course", "Department", "Admission", "Conversation", "Message"]
