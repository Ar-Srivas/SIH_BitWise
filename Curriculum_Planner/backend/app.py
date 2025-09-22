from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.db import Base, engine, SessionLocal
from backend.models import User
from backend.routers import auth_routes, student_routes, quiz_routes, slot_routes, recommend_routes, chat_routes

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# include routers, passing the templates object
app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(quiz_routes.router)
app.include_router(slot_routes.router)
# THIS LINE IS THE FIX. IT CALLS THE FUNCTION.
app.include_router(recommend_routes.create_router(templates))
app.include_router(chat_routes.router)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    if db.query(User).count() == 0:
        db.add_all([
            User(userid="t1", password="pass1", role="teacher"),
            User(userid="s1", password="pass1", role="student"),
            User(userid="s2", password="pass2", role="student"),
        ])
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, email: str = None):
    if not email:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "email": email})

@app.get("/quiz", response_class=HTMLResponse)
def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/slot_booking_students", response_class=HTMLResponse)
def slot_booking_students(request: Request):
    return templates.TemplateResponse("slot_booking_students.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("dummy_chat.html", {"request": request})