from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Mock database (you can replace with real DB later)
teachers = [
    {"id": 1, "name": "Dr. Sharma", "subject": "Mathematics"},
    {"id": 2, "name": "Prof. Iyer", "subject": "Physics"},
    {"id": 3, "name": "Dr. Mehta", "subject": "Chemistry"},
]

slots = []
slot_counter = 1



@app.get("/teachers")
def get_teachers():
    return teachers


@app.get("/slots")
def get_slots():
    return slots


@app.post("/add_slot")
def add_slot(teacher_id: int, slot_date: str, start: str, end: str):
    global slot_counter
    new_slot = {
        "id": slot_counter,
        "teacher_id": teacher_id,
        "date": slot_date,
        "start_time": start,
        "end_time": end,
        "booked": False
    }
    slots.append(new_slot)
    slot_counter += 1
    return {"message": "Slot added", "slot": new_slot}


@app.delete("/delete_slot/{slot_id}")
def delete_slot(slot_id: int):
    global slots
    slots = [s for s in slots if s["id"] != slot_id]
    return {"message": "Slot deleted"}


@app.get("/faculty/slot_management", response_class=HTMLResponse)
def slot_management(request: Request):
    return templates.TemplateResponse("slots.html", {"request": request})
