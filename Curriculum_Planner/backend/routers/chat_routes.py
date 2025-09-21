from fastapi import APIRouter
from backend.controllers.chat_controller import search_chat, send_chat


router=APIRouter()
@router.post("/chat")
async def chat_endpoint(user_message: str):
    search_result = await search_chat(user_message)
    chat_response = await send_chat(search_result, user_message)
    return {"response": chat_response}