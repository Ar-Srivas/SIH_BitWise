from fastapi import APIRouter
from backend.controllers.chat_controller import search_chat, send_chat
from pydantic import BaseModel

class ChatRes(BaseModel):
    user_message:str

router=APIRouter()
@router.post("/chat")
async def chat_endpoint(request: ChatRes):
    search_result = await search_chat(request.user_message)
    chat_response = await send_chat(search_result, request.user_message)
    return {"response": chat_response}