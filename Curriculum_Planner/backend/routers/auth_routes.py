from fastapi import APIRouter
from backend.controllers.auth_controller import signup, login, api_login

router = APIRouter()
router.post("/signup")(signup)
router.post("/login")(login)
router.post("/api/login")(api_login)
