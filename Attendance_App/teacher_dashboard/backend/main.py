from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api import attendance

app = FastAPI(title="dashboard")

app.include_router(attendance.router, prefix="/api")

app.mount("/static", StaticFiles(directory="../frontend", html=True), name="static")

@app.get("/", response_class=FileResponse)
async def serve_login_page():
    return "../frontend/login.html"