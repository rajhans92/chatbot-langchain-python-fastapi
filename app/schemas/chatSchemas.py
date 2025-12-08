from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatHistoryRequest(BaseModel):
    message: str
    chat_history: Optional[List[Dict[str, Any]]] = []


class ChatRequest(BaseModel):
    message: str