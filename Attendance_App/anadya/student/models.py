from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, JSON, Date, Time, ForeignKey, Boolean
from backend.db import Base

# SQL Models
class Student(Base):
    _tablename_ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)  # Email
    grade_level = Column(String)  # Name
    password = Column(String)  # Password
    marks = Column(JSON, nullable=True)
    quiz_answers = Column(JSON, nullable=True)


class Slot(Base):
    _tablename_ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))  # Link to Teacher
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    booked = Column(Boolean, default=False)
    booked_by = Column(Integer, ForeignKey("students.id"), nullable=True)  # Link to student who booked

class Teacher(Base):
    _tablename_ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

# Pydantic Models
class MarksInput(BaseModel):
    grade_level: str
    subjects: Dict[str, int]

class QuizResponse(BaseModel):
    grade_level: str
    answers: List[str]

class StudentProfile(BaseModel):
    grade_level: str
    marks: Optional[Dict[str, int]] = None
    quiz_answers: Optional[List[str]] = None

    class Config:
        from_attributes = True