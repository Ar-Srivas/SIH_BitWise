from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.controllers.academic_controller import academic_assistant

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/academic", response_class=HTMLResponse)
async def get_academic(request: Request):
    return templates.TemplateResponse(
        "academic.html",
        {"request": request, "docs_links": [], "yt_links": [], "query": ""}
    )

@router.post("/academic", response_class=HTMLResponse)
async def post_academic(request: Request, query: str = Form(...)):
    docs_links, yt_links = academic_assistant(query)
    return templates.TemplateResponse(
        "academic.html",
        {"request": request, "docs_links": docs_links, "yt_links": yt_links, "query": query}
    )