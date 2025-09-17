from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import Base, engine, SessionLocal
from .models_faculty import User, Slot
from datetime import datetime
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- API ROUTES ----------
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


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    userid = data.get("userid")
    password = data.get("password")

    print("📩 Received login attempt:", userid, password)

    db = SessionLocal()
    all_users = db.query(User).all()
    print("📋 Users in DB:", [(u.userid, u.password) for u in all_users])

    user = db.query(User).filter_by(userid=userid, password=password).first()
    print("🔍 Query result:", user)
    db.close()

    if user:
        return {"success": True, "role": user.role, "id": user.id}
    else:
        return {"success": False, "message": "Invalid credentials"}


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

# ---------- FRONTEND ----------
frontend_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")
