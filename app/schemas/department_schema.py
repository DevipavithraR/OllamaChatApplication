from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    department_name: str
    description: Optional[str] = None
    head_of_department: Optional[str] = None

class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    description: Optional[str] = None
    head_of_department: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
