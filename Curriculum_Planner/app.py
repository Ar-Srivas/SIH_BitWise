from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Student
import os
import json

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates/signin.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/signup")
def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter(Student.student_id == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = Student(
        student_id=email,
        grade_level=name,
        password=password,
        marks={},
        quiz_answers={}
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url=f"/dashboard?email={email}", status_code=303)

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return RedirectResponse(url=f"/dashboard?email={email}", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(email: str = None):
    if not email:
        return RedirectResponse(url="/", status_code=303)

    with open("templates/dashboard.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/quiz", response_class=HTMLResponse)
def quiz():
    with open("templates/quiz.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/api/profile")
def get_profile(email: str, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user.grade_level,
        "email": user.student_id,
        "quiz_results": user.quiz_answers or {}
    }

@app.get("/profile", response_class=HTMLResponse)
def profile():
    with open("templates/profile.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/submit-quiz")
def submit_quiz(email: str = Form(...), quiz_result: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        new_results = json.loads(quiz_result)

        if user.quiz_answers:
            for category, count in new_results.items():
                if category in user.quiz_answers:
                    user.quiz_answers[category] += count
                else:
                    user.quiz_answers[category] = count
        else:
            user.quiz_answers = new_results

        db.commit()
        return {"status": "success", "message": "Quiz results saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving quiz results: {str(e)}")