from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import settings


engine = create_async_engine(
    settings.database_url().unicode_string(),
    echo = True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionFactory() as session:
        yield session
