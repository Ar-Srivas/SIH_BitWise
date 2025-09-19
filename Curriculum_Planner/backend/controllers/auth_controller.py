from fastapi import Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Student, User

async def api_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    userid = data.get("userid")
    password = data.get("password")

    user = db.query(User).filter(User.userid == userid, User.password == password).first()
    if user:
        return {"success": True, "role": user.role, "id": user.id}
    return {"success": False, "message": "Invalid credentials"}

def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.student_id == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Student(student_id=email, grade_level=name, password=password, marks={}, quiz_answers={})
    db.add(new_user)
    db.commit()
    return RedirectResponse(url=f"/dashboard?email={email}", status_code=303)

def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return RedirectResponse(url=f"/dashboard?email={email}", status_code=303)
