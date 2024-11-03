# app/repositories/tweet_repository.py
from typing import Sequence, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dal.models import Tweet


class TweetRepository:
    @staticmethod
    async def create_tweet(db: AsyncSession, content: str, author: str) -> Tweet:
        tweet = Tweet(content=content, author=author)
        db.add(tweet)
        await db.commit()
        return tweet

    @staticmethod
    async def get_all_tweets(db: AsyncSession) -> Sequence[Tweet]:
        result = await db.execute(select(Tweet))
        return result.scalars().all()

    @staticmethod
    async def like_tweet(db: AsyncSession, tweet_id: int) -> Type[Tweet] | None:
        tweet = await db.get(Tweet, tweet_id)
        tweet.likes += 1
        await db.commit()
        return tweet
