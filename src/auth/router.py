from fastapi import APIRouter, Query
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
async def get_results(
    districts: Optional[List[str]] = Query(None),
    areas: Optional[List[str]] = Query(None),
    addresses: Optional[List[str]] = Query(None)
):
    async with async_session_maker() as session:
        query = select(NewApart).distinct()
        
        if districts:
            query = query.filter(NewApart.district.in_(districts))
        
        if areas:
            query = query.filter(NewApart.area.in_(areas))
        
        if addresses:
            query = query.filter(NewApart.house_address.in_(addresses))
        
        result = await session.execute(query)
        results = result.scalars().all()
        
    return results
