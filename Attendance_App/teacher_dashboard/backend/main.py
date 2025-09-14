from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import attendance

app = FastAPI(title="dashboard")

app.include_router(attendance.router, prefix="/api")

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")