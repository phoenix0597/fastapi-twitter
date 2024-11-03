# app/services/tweet_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tweet_repository import TweetRepository


class TweetService:
    @staticmethod
    async def create_tweet(db: AsyncSession, content: str, author: str):
        return await TweetRepository.create_tweet(db, content, author)

    @staticmethod
    async def like_tweet(db: AsyncSession, tweet_id: int):
        return await TweetRepository.like_tweet(db, tweet_id)
