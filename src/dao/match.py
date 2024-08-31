from database import async_session_maker
from sqlalchemy import select 
from src.models import NewApart

class New:
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(NewApart)
        