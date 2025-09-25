from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.controllers.slot_controller import get_teachers, available_slots, book_slot
router = APIRouter()

@router.get("/teachers")
def get_teachers_route():
    return get_teachers()

@router.get("/available_slots/{date}/{teacher_id}")
def available_slots_route(date: str, teacher_id: str, db: Session = Depends(get_db)):
    return available_slots(date, teacher_id, db)

@router.post("/book_slot")
async def book_slot_route(request: Request):
    return await book_slot(request)
