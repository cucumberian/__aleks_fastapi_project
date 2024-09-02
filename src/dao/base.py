from database import async_session_maker
from sqlalchemy import select, insert

class BaseDAO:
    model = None 
            
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def get_apart_info(cls):
        async with async_session_maker() as session:
            query = select(cls.model).limit(100)
            result = await session.execute(query)
            print(result)
            return result.mappings().all()
        
    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query) 
            await session.commit()
