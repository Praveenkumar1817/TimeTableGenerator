from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class SubjectType(str, enum.Enum):
    THEORY = "THEORY"
    LAB = "LAB"
    SPECIAL_ACTIVITY = "SPECIAL_ACTIVITY"

class DepartmentSettings(Base):
    __tablename__ = "department_settings"
    id = Column(Integer, primary_key=True, index=True)
    working_days = Column(Integer, default=5)
    periods_per_day = Column(Integer, default=7)

class AcademicYear(Base):
    __tablename__ = "academic_years"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    sections = relationship("Section", back_populates="academic_year", cascade="all, delete-orphan")

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))
    academic_year = relationship("AcademicYear", back_populates="sections")
    subject_assignments = relationship("SubjectAssignment", back_populates="section", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    type = Column(Enum(SubjectType), default=SubjectType.THEORY)
    weekly_periods = Column(Integer, default=4)
    maximum_consecutive_periods = Column(Integer, default=1)
    preferred_distribution = Column(JSON, nullable=True)
    assignments = relationship("SubjectAssignment", back_populates="subject")

class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unavailabilities = relationship("FacultyAvailability", back_populates="faculty", cascade="all, delete-orphan")

class FacultyAvailability(Base):
    __tablename__ = "faculty_availability"
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    day = Column(Integer)
    period = Column(Integer)
    faculty = relationship("Faculty", back_populates="unavailabilities")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_lab = Column(Boolean, default=False)
    capacity = Column(Integer, default=60)

class SubjectAssignment(Base):
    __tablename__ = "subject_assignments"
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    faculty_pool = Column(JSON, nullable=True) 
    required_faculty = Column(Integer, default=1)
    eligible_labs = Column(JSON, nullable=True) 
    
    section = relationship("Section", back_populates="subject_assignments")
    subject = relationship("Subject", back_populates="assignments")

class FixedSlot(Base):
    __tablename__ = "fixed_slots"
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    day = Column(Integer)
    period = Column(Integer)
    duration = Column(Integer, default=1)
    activity_name = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    faculty_ids = Column(JSON, nullable=True)

class Timetable(Base):
    __tablename__ = "timetables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    score = Column(Integer)
    metrics = Column(JSON)
    entries = relationship("TimetableEntry", back_populates="timetable", cascade="all, delete-orphan")

class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    id = Column(Integer, primary_key=True, index=True)
    timetable_id = Column(Integer, ForeignKey("timetables.id"))
    section_id = Column(Integer, ForeignKey("sections.id"))
    day = Column(Integer)
    period = Column(Integer)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    activity_name = Column(String, nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    faculty_ids = Column(JSON, nullable=True)
    
    timetable = relationship("Timetable", back_populates="entries")
