# app/schemas/tweet.py
from pydantic import BaseModel, Field, conint
from datetime import datetime


class TweetCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=280)  # Указание ограничения на длину контента


class TweetResponse(BaseModel):
    id: int
    content: str = Field(..., min_length=1, max_length=280)  # Ограничения на длину контента
    author_username: str
    timestamp: datetime
    likes: conint(ge=0)  # Неотрицательное количество лайков
