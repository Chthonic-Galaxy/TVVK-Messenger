from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings


engine = create_async_engine(
    settings.database_url().unicode_string(),
    echo = settings.DB_ECHO,
    pool_size=20,
    max_overflow=40
)

AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionFactory() as session:
        yield session
