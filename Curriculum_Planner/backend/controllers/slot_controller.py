from fastapi import Request
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import Slot, Teacher
from datetime import datetime

# async def create_slot(request: Request):
#     data = await request.json()
#     db = SessionLocal()
#     slot = Slot(
#         teacher_id=data["teacher_id"],
#         date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
#         start_time=datetime.strptime(data["start_time"], "%H:%M").time(),
#         end_time=datetime.strptime(data["end_time"], "%H:%M").time()
#     )
#     db.add(slot)
#     db.commit()
#     db.close()
#     return {"message": "Slot created"}

def get_teachers():
    db = SessionLocal()
    teachers = db.query(Teacher).all()
    db.close()
    return [{"id": t.id, "name": t.name, "subject": t.subject} for t in teachers]

def available_slots(date: str, teacher_id: str, db: Session):
    d = datetime.strptime(date, "%Y-%m-%d").date()
    db = SessionLocal()
    slots = db.query(Slot).filter(Slot.date==d, Slot.teacher_id==teacher_id, Slot.booked==False).all()
    db.close()
    return [{"id": s.id, "start": s.start_time.strftime("%H:%M"), "end": s.end_time.strftime("%H:%M")} for s in slots]

async def book_slot(request: Request):
    data = await request.json()
    db = SessionLocal()
    try:
        slot = db.query(Slot).filter_by(id=data["slot_id"], booked=False).first()
        if not slot:
            return {"success": False, "message": "Slot already booked"}
        slot.booked = True
        slot.booked_by = data["student_id"]
        db.commit()
        return {"success": True, "message": "Slot booked"}
    finally:
        db.close()
