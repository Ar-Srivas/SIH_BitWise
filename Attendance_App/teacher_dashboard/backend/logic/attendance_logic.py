from datetime import datetime
import uuid

from firebase_config.config import db

def _generate_live_token():
    return str(uuid.uuid4())[:8]

def login(teacher_email: str, teacher_password: str):
    try:
        teacher = db.collection("teachers").document(teacher_email).get()
        if not teacher.exists:
            print(f"no teacher found with email {teacher_email}")
            return None
        # print(teacher.get("password"))
        if teacher_password == teacher.get("password"):
            teacher_info = {
                "name": teacher.get("name"),
                "email": teacher.get("email"),
            }
            return teacher_info
        else:
            return None
    except Exception as e:
        print("login logic error", e)
        return None

def get_dates(teacher_email):
    try:
        date_docs = db.collection("teachers").document(teacher_email).collection("attendance_records").stream()
        dates = [date.id for date in date_docs]
        # print(dates)
        return dates
    except Exception as e:
        print("get dates logic error", e)
        return None

def dashboard(teacher_email, date):
    try:
        data = db.collection("teachers").document(teacher_email).collection("attendance_records").document(date).get()
        data = data.to_dict()
        # print(data)
        if not data:
            print("this date or email does not exits")
            return None
        return data
    except Exception as e:
        print("dashboard logic error", e)
        return None

def start_session(teahcer_id: str, date):
    # today = datetime.now().strftime("%Y-%m-%d")
    # print(today)
    # print(teahcer_id)
    initial_qrvalue = teahcer_id + "#" + _generate_live_token()

    student_map = {}
    try:
        students = db.collection("students").stream()
        for student in students:
            student_id = student.id
            student_data = student.to_dict()
            student_name = student_data["name"]
            # print(student_id, student_name)
            student_map[student_id] = {
                "name": student_name,
                "status": "absent",
                "timestamp": None,
            }
        # print(student_map)
    except Exception as e:
        print("fetching students logic error", e)
    print(initial_qrvalue)
    # db.collection("teachers").document(teahcer_id).collection("attendance_records").document(date).update({"qrvalue": initial_qrvalue})
    attendance_doc_path = db.collection("teachers").document(teahcer_id).collection("attendance_records").document(date)
    data = {
        "date": date,
        "is_session_active": True,
        "students": student_map,
        "qrvalue": initial_qrvalue,
    }
    try:
        attendance_doc_path.set(data)
        return {"teacher_id": teahcer_id, "date": date, "initial_qrvalue": initial_qrvalue}
    except Exception as e:
        print("creating session data logic error", e)
        return None

def update_qrvalue(teacher_id, date):
    session_doc_ref = db.collection("teachers").document(teacher_id).collection("attendance_records").document(date)
    # print(teacher_id, date)
    session_doc = session_doc_ref.get()
    is_session_active = session_doc.get("is_session_active")
    # print(is_session_active)
    if is_session_active:
        try:
            new_qrvalue = teacher_id + "#" + _generate_live_token()
            db.collection("teachers").document(teacher_id).collection("attendance_records").document(date).update({"qrvalue": new_qrvalue})
            return {"new_qrvalue": new_qrvalue}
        except Exception as e:
            print("update qrvalue logic error", e)
            return None
    else:
        # print("talkinabeetdonny")
        return {"new_qrvalue": "session_ended"}
    
def end_session(teacher_id, date):
    try:
        db.collection("teachers").document(teacher_id).collection("attendance_records").document(date).update({"is_session_active": False})
        return {"is_session_active": False}
    except Exception as e:
        print("end session logic error")

def hello_world():
    return {"message": "hello world"}