from fastapi import APIRouter
from backend.controllers.student_controller import get_profile
router = APIRouter()
router.get("/api/profile")(get_profile)
