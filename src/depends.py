from dao import dao as dao_module
from dao.user_dao import UserDao
from dao.new_apart_dao import NewApartDao
from db.database import DbManager
from service.user_service import UserService
from service.new_apart_service import NewApartService

from config import Settings


db_manager = DbManager(async_db_url=Settings.DATABASE_URL)
dao = dao_module.Dao(db_manager=db_manager)
user_dao = UserDao(db_manager=db_manager)
user_service = UserService(user_dao=user_dao)


new_apart_dao = NewApartDao(db_manager=db_manager)
new_apart_service = NewApartService(new_apart_dao=new_apart_dao)

def get_new_apart_dao():
    return new_apart_dao

def get_new_apart_service():
    return new_apart_service

def get_db():
    return db_manager


def get_dao():
    return dao


def get_user_dao():
    return user_dao


def get_user_service():
    return user_service
