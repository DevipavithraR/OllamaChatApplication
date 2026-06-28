from typing import Optional
from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    department_name: str
    description: Optional[str] = None

class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
