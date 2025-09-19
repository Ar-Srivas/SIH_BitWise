import json
from fastapi import Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Student

def submit_quiz(email: str = Form(...), quiz_result: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        new_results = json.loads(quiz_result)
        if user.quiz_answers:
            for category, count in new_results.items():
                user.quiz_answers[category] = user.quiz_answers.get(category, 0) + count
        else:
            user.quiz_answers = new_results
        db.commit()
        return {"status": "success", "message": "Quiz results saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving quiz results: {str(e)}")
