from fastapi import APIRouter, HTTPException
from logic import attendance_logic

router = APIRouter()

@router.post("/login")
def login():
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
def get_dates():
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

@router.get("/dashboard")
def dashboard():
    try:
        result = attendance_logic.dashboard("teacherdummy@example.com", "2025-09-13")
        print(result)
        return result
    except Exception as e:
        print("dashboard router error", e)
        return None

@router.post("/session/start")
def start_session():
    try:
        result = attendance_logic.start_session("teacherdummy@example.com")
        return result
    except Exception as e:
        print("session start router error", e)
        return None

@router.post("/session/update-qrvalue")
def update_qrvalue():
    try:
        result = attendance_logic.update_qrvalue("teacherdummy@example.com")
        return result
    except Exception as e:
        print("update qrvalue router error", e)
        return None

@router.get("/hello")
async def hello_world():
    return attendance_logic.hello_world()