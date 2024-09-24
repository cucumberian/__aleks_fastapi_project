import datetime
from typing import Any
from dao.user_dao import UserDao

from schema.user_schema import UserSchemaApiCreate
from schema.user_schema import UserSchemaDb
from schema.user_schema import UserSchemaDbCreate
from schema.user_schema import UserSchemaApi

from auth import auth


class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    async def find_by_id(self, user_id: int):
        user_db = await self.user_dao.find_by_id(user_id=user_id)
        if user_db is None:
            return None
        user = UserSchemaApi.model_validate(
            user_db,
            from_attributes=True,
        )
        return user

    async def find_one(self, **filter: Any):
        user_db = await self.user_dao.find_one(**filter)
        if user_db is None:
            return None
        user = UserSchemaApi.model_validate(
            user_db,
            from_attributes=True,
        )
        return user

    async def get_all(self):
        users = await self.user_dao.get_all()
        users_api = [
            UserSchemaApi.model_validate(row, from_attributes=True) for row in users
        ]
        return users_api

    async def create(self, new_user: UserSchemaApiCreate):
        hashed_password = auth.get_password_hash(password=new_user.password)
        new_user_db = UserSchemaDbCreate(
            email=new_user.email,
            hashed_password=hashed_password,
        )
        user_db = await self.user_dao.create(user_to_create=new_user_db)
        if user_db is None:
            return None
        user = UserSchemaApi.model_validate(user_db, from_attributes=True)
        return user
