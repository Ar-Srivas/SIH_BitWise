from fastapi import APIRouter, HTTPException
from logic import attendance_logic

router = APIRouter()

@router.get("/session/start")
async def start_session():
    try:
        result = attendance_logic.start_session()
        return result
    except Exception as e:
        print("router error", e)

@router.get("/hello")
async def hello_world():
    return attendance_logic.hello_world()