from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain import Faculty, Subject, Section, Room
from app.schemas.domain import FacultyCreate, FacultyResponse, SubjectCreate, SubjectResponse, SectionBase, SectionCreate, SectionResponse, RoomBase, RoomCreate, RoomResponse, AssignmentCreate, AssignmentResponse
from typing import List

router = APIRouter()

@router.get("/faculty", response_model=List[FacultyResponse])
def get_faculty(db: Session = Depends(get_db)):
    return db.query(Faculty).all()

@router.post("/faculty", response_model=FacultyResponse)
def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    db_fac = Faculty(name=faculty.name)
    db.add(db_fac)
    db.commit()
    db.refresh(db_fac)
    return db_fac

@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_sub = Subject(**subject.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("/sections", response_model=List[SectionResponse])
def get_sections(db: Session = Depends(get_db)):
    return db.query(Section).all()

@router.post("/sections", response_model=SectionResponse)
def create_section(section: SectionCreate, db: Session = Depends(get_db)):
    db_sec = Section(**section.dict())
    db.add(db_sec)
    db.commit()
    db.refresh(db_sec)
    return db_sec

@router.get("/rooms", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.post("/rooms", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/assignments", response_model=List[AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    from app.models.domain import SubjectAssignment
    return db.query(SubjectAssignment).all()

@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    from app.models.domain import SubjectAssignment
    db_assign = SubjectAssignment(**assignment.dict())
    db.add(db_assign)
    db.commit()
    db.refresh(db_assign)
    return db_assign

# --- DELETE Endpoints ---
def generic_delete(model, id: int, db: Session):
    obj = db.query(model).filter(model.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return {"status": "deleted"}

@router.delete("/faculty/{id}")
def delete_faculty(id: int, db: Session = Depends(get_db)):
    return generic_delete(Faculty, id, db)

@router.delete("/subjects/{id}")
def delete_subject(id: int, db: Session = Depends(get_db)):
    return generic_delete(Subject, id, db)

@router.delete("/sections/{id}")
def delete_section(id: int, db: Session = Depends(get_db)):
    return generic_delete(Section, id, db)

@router.delete("/rooms/{id}")
def delete_room(id: int, db: Session = Depends(get_db)):
    return generic_delete(Room, id, db)

@router.delete("/assignments/{id}")
def delete_assignment(id: int, db: Session = Depends(get_db)):
    from app.models.domain import SubjectAssignment
    return generic_delete(SubjectAssignment, id, db)
