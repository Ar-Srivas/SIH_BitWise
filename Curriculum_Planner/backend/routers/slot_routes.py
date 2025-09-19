from fastapi import APIRouter
from backend.controllers.slot_controller import create_slot, available_slots, book_slot
router = APIRouter()
router.post("/create_slot")(create_slot)
router.get("/available_slots/{date}")(available_slots)
router.post("/book_slot")(book_slot)
