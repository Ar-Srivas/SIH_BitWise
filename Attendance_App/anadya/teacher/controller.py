# backend/controllers/faculty_controller.py
from fastapi import Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Slot, Teacher
from datetime import datetime

def get_teachers():
    db = SessionLocal()
    teachers = db.query(Teacher).all()
    db.close()
    return [{"id": t.id, "name": t.name, "subject": t.subject} for t in teachers]

# get available slots for a teacher
def available_slots(date: str, teacher_id: int):
    d = datetime.strptime(date, "%Y-%m-%d").date()
    db = SessionLocal()
    slots = db.query(Slot).filter_by(date=d, teacher_id=teacher_id, booked=False).all()
    db.close()
    return [{"id": s.id, "start": s.start_time.strftime("%H:%M"), "end": s.end_time.strftime("%H:%M")} for s in slots]

# creates a new slot
async def create_slot(request: Request):
    data = await request.json()
    db = SessionLocal()
    try:
        slot = Slot(
            teacher_id=data["teacher_id"],
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            start_time=datetime.strptime(data["start_time"], "%H:%M").time(),
            end_time=datetime.strptime(data["end_time"], "%H:%M").time()
        )
        db.add(slot)
        db.commit()
        return {"success": True, "message": "Slot created"}
    finally:
        db.close()

# views their own slots
def get_faculty_slots(teacher_id: int):
    db = SessionLocal()
    slots = db.query(Slot).filter_by(teacher_id=teacher_id).all()
    db.close()
    return [
        {
            "id": s.id,
            "date": s.date.strftime("%Y-%m-%d"),
            "start": s.start_time.strftime("%H:%M"),
            "end": s.end_time.strftime("%H:%M"),
            "booked": s.booked,
            "booked_by": s.booked_by
        } for s in slots
    ]
