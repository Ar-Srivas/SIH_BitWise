from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)  # Use this field in seed
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
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
