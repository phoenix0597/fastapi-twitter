# app/schemas/user.py
from pydantic import BaseModel
from typing import List
from pydantic import ConfigDict


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str


# Схема для чтения пользователя
class UserRead(BaseModel):
    username: str
    following: List[str] = []  # Список имен пользователей, на кого подписан
    followers: List[str] = []  # Список имен пользователей, кто подписан

    model_config = ConfigDict(from_attributes=True)
