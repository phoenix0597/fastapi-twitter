# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    async def register_user(db: AsyncSession, username: str, password: str):
        user = await UserRepository.get_user_by_username(db, username)
        if user:
            raise ValueError("Username already exists")
        return await UserRepository.create_user(db, username, password)

    @staticmethod
    async def follow_user(db: AsyncSession, follower: str, followee: str):
        if follower == followee:
            raise ValueError("Cannot follow yourself")
        await UserRepository.follow_user(db, follower, followee)
        