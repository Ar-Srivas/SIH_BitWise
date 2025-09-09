from fastapi import APIRouter, HTTPException
from logic import attendance_logic

router = APIRouter()

@router.get("/hello")
async def hello_world():
    return attendance_logic.hello_world()