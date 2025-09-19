from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Student

def get_profile(email: str, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "name": user.grade_level,
        "email": user.student_id,
        "quiz_results": user.quiz_answers or {}
    }
