from fastapi import APIRouter, Query, HTTPException, Path
from sqlalchemy import select
from models.new_apart import NewApart
from database import async_session_maker
from typing import List, Optional

router = APIRouter(prefix='/tables', tags=['/tables'])

@router.get("/districts")
async def get_districts():
    async with async_session_maker() as session:
        result = await session.execute(select(NewApart.district).distinct())
        districts = result.scalars().all()
    return districts

@router.get("/areas")
async def get_areas(districts: Optional[List[str]] = Query(None)):
    async with async_session_maker() as session:
        query = select(NewApart.area).distinct()
        if districts:
            query = query.filter(NewApart.district.in_(districts))
        result = await session.execute(query)
        areas = result.scalars().all()
    return areas

@router.get("/house_addresses")
async def get_house_addresses(areas: Optional[List[str]] = Query(None)):
    async with async_session_maker() as session:
        query = select(NewApart.house_address).distinct()
        if areas:
            query = query.filter(NewApart.area.in_(areas))
        result = await session.execute(query)
        house_addresses = result.scalars().all()
    return house_addresses

@router.get("/results")
async def get_apartments(
    page: int = Query(1, ge=1),  # Номер страницы (по умолчанию 1)
    rows_per_page: int = Query(100, ge=1),  # Количество строк на странице (по умолчанию 100)
    districts: str = Query(None),
    areas: str = Query(None),
    addresses: str = Query(None),
):
    async with async_session_maker() as session:
        query = select(NewApart)

        if districts:
            district_list = districts.split(',')
            query = query.filter(NewApart.district.in_(district_list))

        if areas:
            area_list = areas.split(',')
            query = query.filter(NewApart.area.in_(area_list))

        if addresses:
            address_list = addresses.split(',')
            query = query.filter(NewApart.house_address.in_(address_list))

        # Пагинация
        apartments = (await session.execute(query.offset((page - 1) * rows_per_page).limit(rows_per_page))).scalars().all()
        return apartments


@router.get("/results/{apartment_id}")
async def get_apartment_by_id(
    apartment_id: int = Path(..., description="The ID of the apartment to retrieve")
):
    async with async_session_maker() as session:
        query = select(NewApart).where(NewApart.new_apart_id == apartment_id)
        result = await session.execute(query)
        apartment = result.scalars().first()  # Извлекаем первую запись
        if apartment:
            return apartment
        else:
            raise HTTPException(status_code=404, detail="Apartment not found")