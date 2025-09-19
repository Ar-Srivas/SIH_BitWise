from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Student, User, Slot, Teacher
from datetime import datetime
import json

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    if db.query(User).count() == 0:
        db.add_all([
            User(userid="t1", password="pass1", role="teacher"),
            User(userid="s1", password="pass1", role="student"),
            User(userid="s2", password="pass2", role="student"),
        ])
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates/signin.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/signup")
def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter(Student.student_id == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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

@app.post("/api/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    userid = data.get("userid")
    password = data.get("password")

    user = db.query(User).filter(User.userid == userid, User.password == password).first()
    if user:
        return {"success": True, "role": user.role, "id": user.id}
    else:
        return {"success": False, "message": "Invalid credentials"}

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

@app.post("/create_slot")
async def create_slot(request: Request):
    data = await request.json()
    teacher_id = data.get("teacher_id")
    date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    start_time = datetime.strptime(data.get("start_time"), "%H:%M").time()
    end_time = datetime.strptime(data.get("end_time"), "%H:%M").time()

    db = SessionLocal()
    slot = Slot(teacher_id=teacher_id, date=date, start_time=start_time, end_time=end_time)
    db.add(slot)
    db.commit()
    db.close()
    return {"message": "Slot created"}

@app.get("/available_slots/{date}")
def available_slots(date: str):
    d = datetime.strptime(date, "%Y-%m-%d").date()
    db = SessionLocal()
    slots = db.query(Slot).filter_by(date=d, booked=False).all()
    db.close()
    return [
        {
            "id": s.id,
            "start": s.start_time.strftime("%H:%M"),
            "end": s.end_time.strftime("%H:%M")
        } for s in slots
    ]

@app.post("/book_slot")
async def book_slot(request: Request):
    data = await request.json()
    student_id = data.get("student_id")
    slot_id = data.get("slot_id")

    db = SessionLocal()
    slot = db.query(Slot).filter_by(id=slot_id, booked=False).first()
    if not slot:
        db.close()
        return {"success": False, "message": "Slot already booked"}

    slot.booked = True
    slot.booked_by = student_id
    db.commit()
    db.close()
    return {"success": True, "message": "Slot booked"}

# Hardcoded Student Dataset
students = [
    {"id": "DS07", "name": "Siddh Shah", "course": "Data Science",
     "subjects": {"ML": 82, "AI": 78, "DSA": 75, "DBMS": 68, "Time Series": 90, "Cloud Computing": 85}},
]

# Updated Resource Dataset
resources = [
    {"id": 1, "title": "ML Basics (Google Crash Course)", "subject": "ML", "difficulty": "Easy", "article_link": "https://developers.google.com/machine-learning/crash-course", "youtube_link": "https://www.youtube.com/results?search_query=machine+learning+basics"},
    {"id": 2, "title": "Machine Learning (Andrew Ng)", "subject": "ML", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/machine-learning", "youtube_link": "https://www.youtube.com/results?search_query=Andrew+Ng+machine+learning"},
    {"id": 3, "title": "Deep Learning Specialization", "subject": "ML", "difficulty": "Hard", "article_link": "https://www.coursera.org/specializations/deep-learning", "youtube_link": "https://www.youtube.com/results?search_query=deep+learning+specialization"},
    {"id": 4, "title": "AI For Everyone (Andrew Ng)", "subject": "AI", "difficulty": "Easy", "article_link": "https://www.coursera.org/learn/ai-for-everyone", "youtube_link": "https://www.youtube.com/results?search_query=AI+for+everyone"},
    {"id": 5, "title": "edX Artificial Intelligence Courses", "subject": "AI", "difficulty": "Medium", "article_link": "https://www.edx.org/learn/artificial-intelligence", "youtube_link": "https://www.youtube.com/results?search_query=edx+artificial+intelligence"},
    {"id": 6, "title": "Stanford CS221 (AI)", "subject": "AI", "difficulty": "Hard", "article_link": "http://web.stanford.edu/class/cs221/", "youtube_link": "https://www.youtube.com/results?search_query=Stanford+CS221+AI"},
    {"id": 7, "title": "Data Structures (GeeksforGeeks)", "subject": "DSA", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/data-structures/", "youtube_link": "https://www.youtube.com/results?search_query=data+structures+geeksforgeeks"},
    {"id": 8, "title": "Visual Algorithm Explorer (VisuAlgo)", "subject": "DSA", "difficulty": "Medium", "article_link": "https://visualgo.net/en", "youtube_link": "https://www.youtube.com/results?search_query=Visualgo+algorithms"},
    {"id": 9, "title": "Algorithms, Sedgewick & Wayne (Algs4)", "subject": "DSA", "difficulty": "Hard", "article_link": "https://algs4.cs.princeton.edu/home/", "youtube_link": "https://www.youtube.com/results?search_query=Sedgewick+algorithms"},
    {"id": 10, "title": "DBMS Overview (GeeksforGeeks)", "subject": "DBMS", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/what-is-dbms/", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+overview+geeksforgeeks"},
    {"id": 11, "title": "DBMS Tutorials (TutorialsPoint)", "subject": "DBMS", "difficulty": "Medium", "article_link": "https://www.tutorialspoint.com/dbms/index.htm", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+tutorials"},
    {"id": 12, "title": "Relational Databases & SQL (edX)", "subject": "DBMS", "difficulty": "Hard", "article_link": "https://www.edx.org/course/databases-5-sql", "youtube_link": "https://www.youtube.com/results?search_query=relational+databases+sql+edx"},
    {"id": 13, "title": "Time Series Basics (Analytics Vidhya)", "subject": "Time Series", "difficulty": "Easy", "article_link": "https://www.analyticsvidhya.com/blog/2018/02/introduction-to-time-series-forecasting-with-python/", "youtube_link": "https://www.youtube.com/results?search_query=time+series+basics+analytics+vidhya"},
    {"id": 14, "title": "Time Series Analysis (Coursera)", "subject": "Time Series", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/practical-time-series-analysis", "youtube_link": "https://www.youtube.com/results?search_query=time+series+analysis+coursera"},
    {"id": 15, "title": "Forecasting: Principles and Practice (Book)", "subject": "Time Series", "difficulty": "Hard", "article_link": "https://otexts.com/fpp2/", "youtube_link": "https://www.youtube.com/results?search_query=forecasting+principles+and+practice"},
    {"id": 16, "title": "AWS Getting Started", "subject": "Cloud Computing", "difficulty": "Easy", "article_link": "https://aws.amazon.com/getting-started/", "youtube_link": "https://www.youtube.com/results?search_query=AWS+getting+started"},
    {"id": 17, "title": "Azure Fundamentals learning path", "subject": "Cloud Computing", "difficulty": "Medium", "article_link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "youtube_link": "https://www.youtube.com/results?search_query=Azure+fundamentals+learning+path"},
    {"id": 18, "title": "CNCF Cloud Native Certified", "subject": "Cloud Computing", "difficulty": "Hard", "article_link": "https://www.cncf.io/certification/cka/", "youtube_link": "https://www.youtube.com/results?search_query=CNCF+cloud+native+certified"},
]

def recommend(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return []
    recs = []
    for subject, score in student["subjects"].items():
        if score < 70:
            recs.extend([r for r in resources if r["subject"] == subject and r["difficulty"] in ["Easy", "Medium"]])
        elif 70 <= score < 85:
            recs.extend([r for r in resources if r["subject"] == subject])
        else:
            recs.extend([r for r in resources if r["subject"] == subject and r["difficulty"] in ["Medium", "Hard"]])
    return recs

@app.get("/select_subject", response_class=HTMLResponse)
async def select_subject_page(request: Request):
    return templates.TemplateResponse("select_subject.html", {"request": request})

@app.get("/recommend/{student_id}/{subject_name}", response_class=HTMLResponse)
async def get_recommendations_by_subject(request: Request, student_id: str, subject_name: str):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return HTMLResponse("Student not found.", status_code=404)

    all_recs = recommend(student_id)
    subject_recs = [rec for rec in all_recs if rec["subject"] == subject_name]

    return templates.TemplateResponse(
        "recommendations.html",
        {"request": request, "student": student, "recommendations": subject_recs, "selected_subject": subject_name}
    )



@app.get("/slot_booking_students", response_class=HTMLResponse)
async def slot_booking_students(request: Request):
    return templates.TemplateResponse("slot_booking_students.html", {"request": request})

@app.get("/select_subject", response_class=HTMLResponse)
async def select_subject_page(request: Request):
    return templates.TemplateResponse("select_subject.html", {"request": request})