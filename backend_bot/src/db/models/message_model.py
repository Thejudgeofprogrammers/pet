from pydantic import BaseModel, Field
from uuid import uuid4

class Message(BaseModel):
    messageid: str = Field(default_factory=lambda: str(uuid4()))
    userid: str
    text: str
    
    class Config:
        orm_mode = True
