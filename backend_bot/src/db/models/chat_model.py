from pydantic import BaseModel, Field
from uuid import uuid4
from src.db.models.message_model import Message
from typing import List, Optional
from datetime import datetime

class ChatModel(BaseModel):
    chatid: str = Field(default_factory=lambda: str(uuid4()))
    userid: str
    # Find manager
    messages: Optional[List[Message]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        orm_mode = True

