import asyncio

from depends import db_manager
from depends import user_dao
from depends import dao
from depends import get_user_service

from schema.user_schema import UserSchemaDbCreate


async def test_create_user():
    user = await create_user()
    assert user is not None
    print("test_create_user OK")

async def test_get_users(expected_number_of_users: int = 0):
    users = await get_users()
    assert len(users) == expected_number_of_users
    print("test_get_users OK")    

async def test_get_user(user_id: int):
    user = await user_dao.find_by_id(user_id)
    assert user is not None
    print("test_get_user OK")

async def create_user():
    new_user = UserSchemaDbCreate(
        email="mail@mail.com",
        hashed_password="XXXX",
    )
    user = await user_dao.create(new_user)
    return user


async def get_users():
    users = await user_dao.get_all()
    return users


async def get_users_service():
    user_service = get_user_service()
    users = await user_service.get_all()
    return users


async def init_models():
    await dao.drop_tables()
    await dao.create_tables()


async def main():
    await init_models()
    await test_create_user()
    await user_dao.clear_table()
    await test_get_users(expected_number_of_users=0)
    await test_create_user()
    await test_get_users(expected_number_of_users=1)
    await test_get_user(user_id=2)


if __name__ == "__main__":
    asyncio.run(main())
