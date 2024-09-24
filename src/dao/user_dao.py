from typing import Any
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from dao.dao import Dao
from models.user import UserOrm
from schema.user_schema import UserSchemaDb
from schema.user_schema import UserSchemaDbCreate


class UserDao(Dao):
    async def clear_table(self):
        async with self.db_manager.connect() as conn:
            async with conn.begin():
                query = delete(UserOrm)
                await conn.execute(query)
                await conn.commit()

    async def drop_table(self):
        async with self.db_manager.connect() as conn:
            async with conn.begin():
                await conn.run_sync(UserOrm.metadata.drop_all)

    async def create_table(self):
        async with self.db_manager.connect() as connection:
            async with connection.begin():
                await connection.run_sync(UserOrm.metadata.create_all)

    async def find_by_id(self, user_id: int):
        """Возвращает пользователя по user_id если найден, иначе None"""
        async with self.db_manager.session() as session:
            query = select(UserOrm).where(UserOrm.user_id == user_id)
            cursor = await session.execute(query)
            user_orm = cursor.scalar_one_or_none()
            if user_orm is None:
                return None
            user = UserSchemaDb.model_validate(
                obj=user_orm,
                from_attributes=True,
            )
            return user

    async def create(self, user_to_create: UserSchemaDbCreate):
        """
        Возвращает созданного пользователя или None если пользователь уже существует
        """
        async with self.db_manager.session() as session:
            stmt = (
                insert(UserOrm)
                .values(**user_to_create.model_dump(exclude_none=True))
                .returning(UserOrm)
            )
            try:
                cursor = await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                # пользователь уже существует
                return None
            user_dao = cursor.scalar_one_or_none()
            if user_dao is None:
                return None
            user = UserSchemaDb.model_validate(obj=user_dao, from_attributes=True)
            return user

    async def find_one(self, **filter: Any):
        async with self.db_manager.session() as session:
            query = select(UserOrm).filter_by(**filter)
            cursor = await session.execute(query)
            user_orm = cursor.scalar_one_or_none()
            if not user_orm:
                return None
            user = UserSchemaDb.model_validate(
                obj=user_orm,
                from_attributes=True,
            )
            return user

    async def get_info(self):
        async with self.db_manager.session() as session:
            query = select(UserOrm).limit(100)
            cursor = await session.execute(query)
            users_orm = cursor.scalars().all()
            users = [
                UserSchemaDb.model_validate(obj=row, from_attributes=True)
                for row in users_orm
            ]
            return users

    async def get_all(self):
        async with self.db_manager.session() as session:
            query = select(UserOrm).filter_by()
            cursor = await session.execute(query)
            users_orm = cursor.scalars().all()
            users = [
                UserSchemaDb.model_validate(obj=row, from_attributes=True)
                for row in users_orm
            ]
            return users
