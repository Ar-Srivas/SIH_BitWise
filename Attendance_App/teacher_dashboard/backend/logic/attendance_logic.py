from datetime import datetime

from firebase_config.config import db

def start_session():
    today = datetime.now().strftime("%Y-%m-%d")
    print(today)

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
        return student_map
    except Exception as e:
        print("error fetchin students", e)
    
    

def hello_world():
    return {"message": "hello world"}