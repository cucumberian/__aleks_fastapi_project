from sqlalchemy import select

from dao.dao import Dao

from models.new_apart import NewApart
from schema.district_schema import District
from schema.area_schema import Area
from schema.house_address_schema import HouseAddress
from schema.new_apart_schema import NewApartSchema


class NewApartDao(Dao):
    async def get_districts(self):
        async with self.db_manager.session() as session:
            query = select(NewApart.district).distinct()
            cursor = await session.execute(query)
            districts = cursor.scalars().all()
            districts_db = [District(name=row) for row in districts]
            return districts_db

    async def get_areas(self):
        async with self.db_manager.session() as session:
            query = select(NewApart.area).distinct()
            cursor = await session.execute(query)
            areas_orm = cursor.scalars().all()
            areas = [Area(name=row) for row in areas_orm]
            return areas

    async def get_areas_by_districts(self, districts: list[District]):
        async with self.db_manager.session() as session:
            query = (
                select(NewApart.area)
                .distinct()
                .filter(NewApart.district.in_([d.name for d in districts]))
            )
            cursor = await session.execute(query)
            areas_orm = cursor.scalars().all()
            areas = [Area(name=row) for row in areas_orm]
            return areas

    async def get_house_addresses(self):
        async with self.db_manager.session() as session:
            query = select(NewApart.house_address).distinct()
            cursor = await session.execute(query)
            houses_str = cursor.scalars().all()
            house_addresses = [HouseAddress(address=row) for row in houses_str]
            return house_addresses

    async def get_house_addresses_by_areas(self, areas: list[Area]):
        async with self.db_manager.session() as session:
            query = (
                select(NewApart.house_address)
                .distinct()
                .filter(NewApart.area.in_([a.name for a in areas]))
            )
            cursor = await session.execute(query)
            houses_str = cursor.scalars().all()
            house_addresses = [HouseAddress(address=row) for row in houses_str]
            return house_addresses

    async def get_apartment_by_id(self, apartment_id: int):
        async with self.db_manager.session() as session:
            query = select(NewApart).where(NewApart.new_apart_id == apartment_id)
            cursor = await session.execute(query)
            apartment_orm = cursor.scalar_one_or_none()
            if apartment_orm is None:
                return None
            apartment = NewApartSchema.model_validate(
                apartment_orm, from_attributes=True
            )
            return apartment

    async def get_apartments(
        self,
        page: int,
        rows_per_page: int,
        districts: list[District] | None = None,
        areas: list[Area] | None = None,
        addresses: list[HouseAddress] | None = None,
    ):
        async with self.db_manager.session() as session:
            query = select(NewApart)

            # это условие не будет нормально работать, т.к. тут И
            # и нет ни одной квартиры, которая находилась бы одновременно в двух разных адресах
            # а надо ИЛИ по разным адресам, которые делятся по своим area, которые делятся по своим disctricts
            # нужно впиливать связи district -> area -> address -> apartment
            # иначе чтобы это всё работало нужны уникальные названия адреcов в каждой area 
            # и уникальные названия area в каждом district
            if districts:
                district_set = {d.name for d in districts}
                query = query.filter(NewApart.district.in_(district_set))
            if areas:
                areas_set = {a.name for a in areas}
                query = query.filter(NewApart.area.in_(areas_set))
            if addresses:
                address_set = {a.address for a in addresses}
                query = query.filter(NewApart.house_address.in_(address_set))
            # compiled_query = query.compile(compile_kwargs={"literal_binds": True})
            # print("query: ", compiled_query)
            cursor = await session.execute(
                query.offset((page - 1) * rows_per_page).limit(rows_per_page)

            )
            apartments_orm = cursor.scalars().all()
            apartments = [
                NewApartSchema.model_validate(row, from_attributes=True)
                for row in apartments_orm
            ]
            # print(f"{apartments = }")
            return apartments
