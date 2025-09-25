from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, JSON, Date, Time, ForeignKey, Boolean
from backend.db import Base

# SQL Models
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)  # Email
    grade_level = Column(String)  # Name
    password = Column(String)  # Password
    marks = Column(JSON, nullable=True)
    quiz_answers = Column(JSON, nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "teacher" or "student"

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    booked = Column(Boolean, default=False)
    booked_by = Column(Integer, ForeignKey("users.id"), nullable=True)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(String, primary_key=True, index=True)
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