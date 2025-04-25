from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class Message(BaseModel):
    messageid: str = Field(default_factory=lambda: str(uuid4()))
    userid: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        orm_mode = True
