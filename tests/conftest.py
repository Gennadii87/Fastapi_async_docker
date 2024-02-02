from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import conn_url

test_engine = create_async_engine(conn_url)

TestAsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=test_engine)

pytest_plugins = 'tests.fixtures'


async def test_init_db():
    """Возвращает соединение с базой данных."""
    async with TestAsyncSessionLocal() as async_session:
        yield async_session
