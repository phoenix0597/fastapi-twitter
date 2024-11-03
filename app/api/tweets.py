# app/api/tweets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.tweet_service import TweetService
from app.schemas.tweet import TweetCreate, TweetResponse
from app.dal.database import get_session

router = APIRouter()


@router.post("/", response_model=TweetResponse)
async def create_tweet(tweet: TweetCreate, author: str, db: AsyncSession = Depends(get_session)):
    return await TweetService.create_tweet(db, tweet.content, author)


@router.post("/{tweet_id}/like", response_model=TweetResponse)
async def like_tweet(tweet_id: int, db: AsyncSession = Depends(get_session)):
    try:
        return await TweetService.like_tweet(db, tweet_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Tweet not found")
