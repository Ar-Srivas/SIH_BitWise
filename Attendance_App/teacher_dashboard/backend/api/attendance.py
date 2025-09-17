from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from logic import attendance_logic

router = APIRouter()

class TeacherLogin(BaseModel):
    email: str
    password: str

class SessionInfo(BaseModel):
    teacher_id: str
    date: str

@router.post("/login")
def login(teacher_data: TeacherLogin):
    try:
        result = attendance_logic.login(teacher_data.email, teacher_data.password)
        if result:
            # print(result)
            return result
        # print(result)
        return None
    except Exception as e:
        print("login router error", e)
        return None

@router.get("/dates")
def get_dates(teacher_id: str = Query(...)):
    try:
        result = attendance_logic.get_dates(teacher_id)
        # print(result)
        return result if result is not None else []
    except Exception as e:
        print("get dates router error", e)
        return None

@router.get("/dashboard")
def dashboard(teacher_id: str = Query(...), date: str = Query(...)):
    try:
        result = attendance_logic.dashboard(teacher_id, date)
        print(result)
        return result
    except Exception as e:
        print("dashboard router error", e)
        return None

@router.post("/session/start")
def start_session(session_data: SessionInfo):
    try:
        result = attendance_logic.start_session(session_data.teacher_id, session_data.date)
        return result
    except Exception as e:
        print("session start router error", e)
        return None

@router.post("/session/update-qrvalue")
def update_qrvalue(session_data: SessionInfo):
    try:
        result = attendance_logic.update_qrvalue(session_data.teacher_id, session_data.date)
        return result
    except Exception as e:
        print("update qrvalue router error", e)
        return None
    
@router.post("/session/end")
def end_session(session_data: SessionInfo):
    try:
        # print("your mother")
        result = attendance_logic.end_session(session_data.teacher_id, session_data.date)
        # print(result)
        return result
    except Exception as e:
        print("end session router error", e)
        return None

@router.get("/hello")
async def hello_world():
    return attendance_logic.hello_world()