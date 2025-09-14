from datetime import datetime
import random
import string

from firebase_config.config import db

def generate_rand_string_helper(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

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
        print(dates)
        return dates
    except Exception as e:
        print("get dates logic error", e)
        return None

def dashboard(teacher_email, date):
    try:
        data = db.collection("teachers").document(teacher_email).collection("attendance_records").document(date).get()
        data = data.to_dict()
        print(data)
        if not data:
            print("this date or email does not exits")
            return None
        return data
    except Exception as e:
        print("dashboard logic error", e)
        return None

def start_session(teahcer_id: str):
    today = datetime.now().strftime("%Y-%m-%d")
    print(today)
    print(teahcer_id)
    qrvalue = teahcer_id + "#" + generate_rand_string_helper(5)

    student_map = {}
    try:
        students = db.collection("students").stream()
        for student in students:
            student_id = student.id
            student_data = student.to_dict()
            student_name = student_data["name"]
            print(student_id, student_name)
            student_map[student_id] = {
                "name": student_name,
                "status": "absent",
                "timestamp": None,
            }
        print(student_map)
    except Exception as e:
        print("fetching students logic error", e)

    db.collection("teachers").document(teahcer_id).set({"qrvalue": qrvalue}, merge=True)
    attendance_doc_path = db.collection("teachers").document(teahcer_id).collection("attendance_records").document(today)
    data = {
        "date": today,
        "is_session_active": True,
        "students": student_map,
    }
    try:
        attendance_doc_path.set(data)
        return data
    except Exception as e:
        print("creating session data logic error", e)

def hello_world():
    return {"message": "hello world"}