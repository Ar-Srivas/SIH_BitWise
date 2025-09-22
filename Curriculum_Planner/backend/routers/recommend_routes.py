from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from backend.controllers import recommend_controller

def create_router(templates: Jinja2Templates):
    router = APIRouter()
    
    @router.get("/select_subject/{student_id}")
    async def select_subject_route(request: Request, student_id: str):
        return await recommend_controller.select_subject_page(request, student_id, templates)

    @router.get("/recommend/{student_id}/{subject_name}")
    async def get_recommendations_route(request: Request, student_id: str, subject_name: str):
        return await recommend_controller.get_recommendations_page(request, student_id, subject_name, templates)
        
    return router