from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Student
from fastapi.staticfiles import StaticFiles
import os

'''
THIS FILE IS THE ENTRY POINT OF THE APPLICATION
MAKE YOUR ROUTES HERE AND LINK THEM TO THE APPROPRIATE FILES IN THE FOLDER
'''

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mount static files
app.mount("/frontend", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "frontend")), name="frontend")

@app.get("/", response_class=HTMLResponse)
def root():
    with open(os.path.join(os.path.dirname(__file__), "frontend/signin.html"), "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/signup")
def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter(Student.student_id == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = Student(student_id=email, grade_level=name, password=password, marks={}, quiz_answers=[])
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.student_id == email).first()
    if not user or user.password != password:  # Simple password check without hashing
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open(os.path.join(os.path.dirname(__file__), "frontend/dashboard.html"), "r") as file:
        return HTMLResponse(content=file.read())
