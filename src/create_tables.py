import asyncio

from db.database import DbManager
from config import Settings

from dao.dao import Dao


async def init_models():
    db_manager = DbManager(async_db_url=Settings.DATABASE_URL)
    dao = Dao(db_manager=db_manager)
    await dao.drop_tables()
    await dao.create_tables()

if __name__ == "__main__":
    asyncio.run(init_models())
