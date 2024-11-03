# app/dal/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)

    # Связи с твитами и подписками
    tweets = relationship("Tweet", back_populates="user")
    following = relationship("Follow",
                             foreign_keys="Follow.follower_username",
                             back_populates="follower")
    followers = relationship("Follow",
                             foreign_keys="Follow.followee_username",
                             back_populates="followee")


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(280), nullable=False)  # Ограничение по длине контента
    author_username = Column(String, ForeignKey("users.username"), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    likes = Column(Integer, default=0)

    user = relationship("User", back_populates="tweets")


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)
    follower_username = Column(String, ForeignKey("users.username"), nullable=False)
    followee_username = Column(String, ForeignKey("users.username"), nullable=False)

    # Уникальность пары подписчик-подписка
    __table_args__ = (UniqueConstraint('follower_username', 'followee_username', name='uix_1'),)

    # Связи с пользователями
    follower = relationship("User",
                            foreign_keys=[follower_username],
                            back_populates="following")
    followee = relationship("User",
                            foreign_keys=[followee_username],
                            back_populates="followers")
