from fastapi import APIRouter
from pydantic import BaseModel
from backend.controllers.chat_controller import search_chat, send_chat

class ChatRequest(BaseModel):
    user_message: str

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        print(f"Received message: {request.user_message}")  # Debug log

        search_result = await search_chat(request.user_message)
        chat_response = await send_chat(search_result, request.user_message)

        print(f"Generated response: {chat_response[:100]}...")  # Debug log

        return {"response": chat_response}
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return {"response": "I'm sorry, I'm having trouble processing your request right now. Please try again."}