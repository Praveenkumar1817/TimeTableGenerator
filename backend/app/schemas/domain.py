from pydantic import BaseModel
from typing import List, Optional

class FacultyBase(BaseModel):
    name: str

class FacultyCreate(FacultyBase):
    pass

class FacultyResponse(FacultyBase):
    id: int
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    type: str = "THEORY"
    weekly_periods: int = 4

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    class Config:
        from_attributes = True

class SectionBase(BaseModel):
    name: str

class SectionCreate(SectionBase):
    pass

class SectionResponse(SectionBase):
    id: int
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str
    is_lab: bool = False
    capacity: int = 60

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    section_id: int
    subject_id: int
    faculty_pool: Optional[str] = "[]"
    required_faculty: int = 1
    eligible_labs: Optional[str] = "[]"

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    class Config:
        from_attributes = True
