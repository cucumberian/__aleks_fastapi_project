import pytest
import pytest_asyncio

from dao.user_dao import UserDao
from dao.dao import Dao
from db.database import DbManager

from config import Settings


t_db_manager = DbManager(async_db_url=Settings.DATABASE_URL)
t_dao = Dao(db_manager=t_db_manager)
t_user_dao = UserDao(db_manager=t_db_manager)




@pytest.fixture(scope="session")
def db_manager():
    yield t_db_manager


@pytest.fixture(scope="session")
def dao(db_manager: DbManager):
    return t_dao


@pytest.fixture(scope="session")
def user_dao(db_manager: DbManager):
    return t_user_dao



@pytest_asyncio.fixture(scope="function")
async def recreate_tables(dao: "Dao"):
    await dao.drop_tables()
    await dao.create_tables()
