# app/main.py
from fastapi import FastAPI
from app.api import users, tweets

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tweets.router, prefix="/tweets", tags=["tweets"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
