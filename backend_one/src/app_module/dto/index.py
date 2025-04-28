from datetime import datetime, date
from pydantic import BaseModel


class VideoDTO(BaseModel):
    id: int
    title: str
    description: str
    video_url: str
    date_uploaded: datetime


class ArticleDTO(BaseModel):
    id: int
    title: str
    description: str
    date_uploaded: datetime


class RequestUserDTO(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: str
    date: date
    
class Operator(BaseModel):
    id: int
    login: str
    password: str