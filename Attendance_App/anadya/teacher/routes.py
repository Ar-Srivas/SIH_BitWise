from fastapi import APIRouter
from controller import (
    available_slots, create_slot, get_teachers, get_faculty_slots
)

router = APIRouter()

router.get("/teachers")(get_teachers)
router.get("/available_slots/{date}/{teacher_id}")(available_slots)
router.post("/create_slot")(create_slot)
router.get("/faculty_slots/{teacher_id}")(get_faculty_slots)
from fastapi import APIRouter
from controller import (
    available_slots, create_slot, get_teachers, get_faculty_slots
)

router = APIRouter()

router.get("/teachers")(get_teachers)
router.get("/available_slots/{date}/{teacher_id}")(available_slots)
router.post("/create_slot")(create_slot)
router.get("/faculty_slots/{teacher_id}")(get_faculty_slots)
