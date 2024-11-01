from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

app = FastAPI()

# Since we can't use a real database, we'll use simple file storage
DATA_FILE = "data.json"


class Tweet(BaseModel):
    id: int
    content: str
    author: str
    timestamp: str
    likes: int = 0


class User(BaseModel):
    username: str
    password: str
    following: List[str] = []


def load_data():
    if not Path(DATA_FILE).exists():
        return {"tweets": [], "users": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# User routes
@app.post("/users/register")
async def register_user(username: str, password: str):
    data = load_data()
    if username in data["users"]:
        raise HTTPException(status_code=400, detail="Username already exists")

    data["users"][username] = {
        "password": password,
        "following": []
    }
    save_data(data)
    return {"message": "User registered successfully"}


@app.post("/users/login")
async def login_user(username: str, password: str):
    data = load_data()
    if username not in data["users"] or data["users"][username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}


# Tweet routes
@app.post("/tweets")
async def create_tweet(content: str, username: str):
    data = load_data()
    if username not in data["users"]:
        raise HTTPException(status_code=404, detail="User not found")

    tweet = {
        "id": len(data["tweets"]),
        "content": content,
        "author": username,
        "timestamp": datetime.now().isoformat(),
        "likes": 0
    }
    data["tweets"].append(tweet)
    save_data(data)
    return tweet


@app.get("/tweets")
async def get_tweets(username: Optional[str] = None):
    data = load_data()
    if username:
        return [t for t in data["tweets"] if t["author"] == username]
    return data["tweets"]


@app.post("/tweets/{tweet_id}/like")
async def like_tweet(tweet_id: int, username: str):
    data = load_data()
    for tweet in data["tweets"]:
        if tweet["id"] == tweet_id:
            tweet["likes"] += 1
            save_data(data)
            return tweet
    raise HTTPException(status_code=404, detail="Tweet not found")


# Following functionality
@app.post("/users/{username}/follow")
async def follow_user(username: str, follower: str):
    data = load_data()
    if username not in data["users"] or follower not in data["users"]:
        raise HTTPException(status_code=404, detail="User not found")

    if username == follower:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    if username not in data["users"][follower]["following"]:
        data["users"][follower]["following"].append(username)
        save_data(data)
    return {"message": f"Now following {username}"}


@app.get("/feed/{username}")
async def get_feed(username: str):
    data = load_data()
    if username not in data["users"]:
        raise HTTPException(status_code=404, detail="User not found")

    following = data["users"][username]["following"]
    feed = [t for t in data["tweets"] if t["author"] in following or t["author"] == username]
    return sorted(feed, key=lambda x: x["timestamp"], reverse=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)