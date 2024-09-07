from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import Settings

schema = Settings.DB_SCHEMA

engine = create_async_engine(Settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
