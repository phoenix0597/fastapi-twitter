from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func

Base = DeclarativeBase()


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    following = relationship("Follow", back_populates="follower")


class Tweet(Base):
    __tablename_ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author = Column(String, ForeignKey("users.username"), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    likes = Column(Integer, default=0)


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)
    follower_username = Column(String, ForeignKey("users.username"), nullable=False)
    followee_username = Column(String, ForeignKey("users.username"), nullable=False)
    follower = relationship("User", foreign_keys=[follower_username], back_populates="following")
    followee = relationship("User", foreign_keys=[followee_username])
