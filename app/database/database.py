from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import conn_url

Base = declarative_base()


engine = create_async_engine(conn_url, echo=True)


SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=engine)


async def init_db():
    """Создание таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Возвращает соединение с базой данных."""
    async with SessionLocal() as async_session:
        yield async_session
