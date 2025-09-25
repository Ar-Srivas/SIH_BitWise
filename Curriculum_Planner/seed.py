from backend.db import SessionLocal, engine
from backend.models import Base, Teacher, Slot
from datetime import date, time

# Create all database tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Create Dummy Teachers ---
# Check if teachers already exist to avoid duplicates
if db.query(Teacher).count() == 0:
    print("Creating dummy teachers...")
    # This now uses the Teacher model directly
    teacher1 = Teacher(id="prof.snape@hogwarts.edu", name="Prof. Severus Snape", subject="Potions")
    teacher2 = Teacher(id="prof.mcgonagall@hogwarts.edu", name="Prof. Minerva McGonagall", subject="Transfiguration")
    db.add_all([teacher1, teacher2])
    db.commit()
    print("Dummy teachers created.")
else:
    print("Teachers already exist.")
    teacher1 = db.query(Teacher).filter_by(id="prof.snape@hogwarts.edu").first()
    teacher2 = db.query(Teacher).filter_by(id="prof.mcgonagall@hogwarts.edu").first()


# --- Create Dummy Slots ---
# Check if slots exist to avoid duplicates
if db.query(Slot).count() == 0:
    print("Creating dummy slots...")
    # This now correctly uses the string ID from the Teacher objects
    slots_to_add = [
        # Snape's slots
        Slot(teacher_id=teacher1.id, date=date(2025, 9, 29), start_time=time(10, 0), end_time=time(10, 30)),
        Slot(teacher_id=teacher1.id, date=date(2025, 9, 29), start_time=time(10, 30), end_time=time(11, 0)),
        # McGonagall's slots
        Slot(teacher_id=teacher2.id, date=date(2025, 9, 29), start_time=time(14, 0), end_time=time(14, 30)),
        Slot(teacher_id=teacher2.id, date=date(2025, 9, 30), start_time=time(11, 0), end_time=time(11, 30)),
    ]
    db.add_all(slots_to_add)
    db.commit()
    print("Dummy slots created.")
else:
    print("Slots already exist.")

db.close()

