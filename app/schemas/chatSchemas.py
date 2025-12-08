from pydantic import BaseModel
from typing import List, Dict, Any


class ChatHistoryRequest(BaseModel):
    message: str
    chat_history: List[Dict[str, Any]]


class ChatRequest(BaseModel):
    message: str