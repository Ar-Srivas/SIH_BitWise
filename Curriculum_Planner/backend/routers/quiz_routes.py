from fastapi import APIRouter
from backend.controllers.quiz_controller import submit_quiz
router = APIRouter()
router.post("/submit-quiz")(submit_quiz)
