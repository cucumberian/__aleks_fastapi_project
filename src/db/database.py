import contextlib
from typing import Any
from typing import AsyncGenerator
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


from config import Settings

schema = Settings.DB_SCHEMA

async_engine = create_async_engine(
    url=Settings.DATABASE_URL,
    # echo=True,
)
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass


class DbManager:
    """
    Класс для управления подключением к базе данных и создания сессий

    .session() - асинхронный генератор сессий
    .connect() - асинхронный генератор подключений
    """

    def __init__(self, async_db_url: str):
        self.async_engine = create_async_engine(
            url=async_db_url,
            # echo=True,
        )
        self.async_session_maker = sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @contextlib.asynccontextmanager
    async def connect(self):
        async with self.async_engine.connect() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
            finally:
                await connection.close()

    async def create_all(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_schema(self):
        async with self.async_engine.begin() as conn:
            await conn.execute(CreateSchema(name=schema, if_not_exists=True))
