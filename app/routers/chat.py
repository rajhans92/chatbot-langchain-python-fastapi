from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.helpers.database import get_db
from app.helpers.jwt import get_current_user
from app.models.chatHistoryModel import ChatHistory
from app.ai.chatAI import chatbot
from app.schemas.chatSchemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/ai")
def chat_endpoint(message: ChatRequest, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    print("message ", message.message)
    chatHistory = db.query(ChatHistory.role, ChatHistory.message).filter(ChatHistory.user_id == user.id).all()

    ai_response = chatbot(message,chatHistory)

    db.add(ChatHistory(
        user_id=user.id,
        role="user",
        message=message.message
    ))

    db.add(ChatHistory(
        user_id=user.id,
        role="assistant",
        message=ai_response
    ))

    db.commit()

    return {"response": ai_response}

@router.get("/history")
def get_chat_history(limit: int = 20, offset:int = 0,user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user.id).order_by(ChatHistory.created_at.asc()).offset(offset).limit(limit).all()
    history = [{"role": chat.role, "message": chat.message, "timestamp": chat.created_at} for chat in chat_history]
    return {"chat_history": history}
