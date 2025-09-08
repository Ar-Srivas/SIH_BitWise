from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, JSON
from db import Base
'''
FOR DB MANAGEMENT
'''


# SQL Models
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)  # Email
    grade_level = Column(String)  # Name
    password = Column(String)  # Password
    marks = Column(JSON, nullable=True)
    quiz_answers = Column(JSON, nullable=True)


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
        from_attributes = True  # Changed from orm_mode to fix the warning