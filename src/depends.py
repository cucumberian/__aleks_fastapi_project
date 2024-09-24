from dao import dao as dao_module
from dao.user_dao import UserDao
from db.database import DbManager
from service.user_service import UserService

from config import Settings

db_manager = DbManager(async_db_url=Settings.DATABASE_URL)
dao = dao_module.Dao(db_manager=db_manager)
user_dao = UserDao(db_manager=db_manager)
user_service = UserService(user_dao=user_dao)


def get_db():
    return db_manager


def get_dao():
    return dao


def get_user_dao():
    return user_dao


def get_user_service():
    return user_service
