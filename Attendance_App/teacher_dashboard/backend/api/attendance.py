from fastapi import APIRouter, HTTPException
from logic import attendance_logic

router = APIRouter()

@router.get("/login")
async def login():
    try:
        result = attendance_logic.login("teacherdummy@example.com", "teacherdummy123")
        if result:
            print(result)
            return result
        print(result)
        return None
    except Exception as e:
        print("login router error", e)
        return None

@router.get("/dates")
async def get_dates():
    try:
        result = attendance_logic.get_dates("teacherdummy@example.com")
        print(result)
        if not result:
            print("no dates found")
            return None
        return result
    except Exception as e:
        print("get dates router error", e)
        return None
        

@router.get("/session/start")
async def start_session():
    try:
        result = attendance_logic.start_session("teacherdummy@example.com")
        return result
    except Exception as e:
        print("session start router error", e)

@router.get("/hello")
async def hello_world():
    return attendance_logic.hello_world()