# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserRead
from app.dal.database import get_session

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        await UserService.register_user(db, user.username, user.password)
        return {"username": user.username, "following": []}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{username}/follow")
async def follow_user(username: str, follower: str, db: AsyncSession = Depends(get_session)):
    try:
        await UserService.follow_user(db, follower, username)
        return {"message": f"{follower} now follows {username}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
