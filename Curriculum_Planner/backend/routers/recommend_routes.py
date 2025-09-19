from fastapi import APIRouter
from backend.controllers.recommend_controller import select_subject_page, get_recommendations_by_subject
router = APIRouter()
router.get("/select_subject")(select_subject_page)
router.get("/recommend/{student_id}/{subject_name}")(get_recommendations_by_subject)
