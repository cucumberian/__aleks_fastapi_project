from sqlalchemy import select

from dao.dao import Dao

from models.new_apart import NewApart
from schema.district_schema import District


class DistrictDao(Dao):
    async def get_all(self):
        async with self.db_manager.session() as session:
            query = select(NewApart.district).distinct()
            cursor = await session.execute(query)
            districts = cursor.scalars().all()
            districts_db = [District(district=row) for row in districts]
            return districts_db
