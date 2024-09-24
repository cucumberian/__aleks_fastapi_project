import pytest
import pytest_asyncio
from schema.user_schema import UserSchemaDbCreate

from dao.user_dao import UserDao
from dao.dao import Dao

from config import Settings
from db.database import DbManager



# @pytest.mark.asyncio(loop_scope="function")
# async def test_empty_users(
#     # event_loop,
#     user_dao: UserDao,
# ):
#     users = await user_dao.get_all()
#     assert len(users) == 0


@pytest.mark.asyncio(loop_scope="function")
async def test_create_user(
    # event_loop,
    user_dao: UserDao,
    recreate_tables,
):
    new_user = UserSchemaDbCreate(
        email="test@test.email",
        hashed_password="hashed_testtest",
    )
    created_user = await user_dao.create(user_to_create=new_user)
    print("\ncreated_user =", created_user)
    assert created_user is not None
    assert 1 == 1
