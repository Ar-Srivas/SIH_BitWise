from fastapi import APIRouter
from backend.controllers.slot_controller import available_slots, book_slot, get_teachers

router = APIRouter()

router.get("/available_slots/{date}/{teacher_id}", response_model=list)(available_slots)
router.post("/book_slot")(book_slot)
router.get("/teachers", response_model=list)(get_teachers)