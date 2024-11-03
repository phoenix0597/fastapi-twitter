# app/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dal.models import User, Follow


class UserRepository:
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, username: str, password: str) -> User:
        user = User(username=username, password=password)
        db.add(user)
        await db.commit()
        return user

    @staticmethod
    async def follow_user(db: AsyncSession, follower: str, followee: str) -> None:
        follow = Follow(follower_username=follower, followee_username=followee)
        db.add(follow)
        await db.commit()