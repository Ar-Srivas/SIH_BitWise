from .database import SessionLocal, engine
from .models_faculty import Base, User, Teacher

Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Only add users if table is empty
if session.query(User).count() == 0:
    users = [
        User(userid="t1", password="pass1", role="teacher"),
        User(userid="t2", password="pass2", role="teacher"),
        User(userid="s1", password="pass3", role="student"),
    ]
    session.add_all(users)

# Only add teachers if table is empty
if session.query(Teacher).count() == 0:
    teachers = [
        Teacher(name="Teacher 1", subject="Math"),
        Teacher(name="Teacher 2", subject="Science"),
    ]
    session.add_all(teachers)

session.commit()
session.close()
