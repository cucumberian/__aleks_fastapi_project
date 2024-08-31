from fastapi import APIRouter
from src.database import schema, async_session_maker
from sqlalchemy import text

new_aparts = APIRouter(
    prefix='/new_aparts',
    tags=['new_aparts']
)

@new_aparts.get('/')
async def get_unique_new_apart():
    async with async_session_maker() as session:
        query = (text(f'SELECT * FROM {schema}.new_apart'))
        result = await session.execute(query)
        return result.mappings().all()
    