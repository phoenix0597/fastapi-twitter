from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


async_engine: AsyncEngine = create_async_engine(settings.DB_URL)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
