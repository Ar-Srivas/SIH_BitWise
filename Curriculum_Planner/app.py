from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Student, MarksInput, QuizResponse
'''
THIS FILE IS THE ENTRY POINT OF THE APPLICATION
MAKE YOUR ROUTES HERE AND LINK THEM TO THE APPROPRIATE FILES IN THE FOLDER

'''
app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello from Curriculum Planning API"}

# Submit Quiz Answers
@app.post("/onboarding/quiz")
def submit_quiz(student_id: str, data: QuizResponse, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(student_id=student_id, grade_level=data.grade_level, marks={}, quiz_answers=data.answers)
        db.add(student)
    else:
        student.grade_level = data.grade_level
        student.quiz_answers = data.answers
    db.commit()
    db.refresh(student)
    return {"message": "Quiz submitted successfully", "student": student.student_id}

# Get Profile
@app.get("/profile/{student_id}")
def get_profile(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    return {
        "student_id": student.student_id,
        "grade_level": student.grade_level,
        "marks": student.marks,
        "quiz_answers": student.quiz_answers,
    }
