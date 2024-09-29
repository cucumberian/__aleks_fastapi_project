from fastapi import APIRouter, Query, HTTPException, Path, Depends
from fastapi import Body

from schema.district_schema import District
from schema.area_schema import Area
from schema.house_address_schema import HouseAddress
from auth.auth import get_current_user
from dao.new_apart_dao import NewApartDao
from depends import get_new_apart_dao
from schema.new_apart_schema import NewApartSchema


router = APIRouter(
    prefix="/tables",
    tags=["/tables"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/districts", response_model=list[str])
@router.post("/districts", response_model=list[str])
async def get_districts(
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    districts = await new_apart_dao.get_districts()
    return [d.name for d in districts]


@router.get("/areas", response_model=list[str])
@router.post("/areas", response_model=list[str])
async def get_areas(
    districts: list[str] | None = Body(default=None),
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    if districts is None:
        areas = await new_apart_dao.get_areas()
    else:
        districts_schema = [District(name=i) for i in districts]
        areas = await new_apart_dao.get_areas_by_districts(districts=districts_schema)
    return [a.name for a in areas]


@router.get("/house_addresses", response_model=list[str])
@router.post("/house_addresses", response_model=list[str])
async def get_house_addresses(
    areas: list[str] | None = Body(default=None),
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    if areas is None:
        house_addresses = await new_apart_dao.get_house_addresses()
    else:
        areas_schema = [Area(name=a) for a in areas]
        house_addresses = await new_apart_dao.get_house_addresses_by_areas(
            areas=areas_schema,
        )
    return [h.address for h in house_addresses]


@router.post("/apartments")
async def get_new_apartments(
    page: int = Query(1, ge=1),  # Номер страницы (по умолчанию 1)
    rows_per_page: int = Query(default=100, ge=1),
    districts: list[str] | None = Body(default=None),
    areas: list[str] | None = Body(default=None),
    addresses: list[str] | None = Body(default=None),
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    districts_schema = [District(name=d) for d in districts] if districts else None
    areas_schema = [Area(name=a) for a in areas] if areas else None
    addresses_schema = (
        [HouseAddress(address=a) for a in addresses] if addresses else None
    )
    # new_apart_dao.db_manager.async_engine.echo = True
    apartments = await new_apart_dao.get_apartments(
        page=page,
        rows_per_page=rows_per_page,
        districts=districts_schema,
        areas=areas_schema,
        addresses=addresses_schema,
    )
    # new_apart_dao.db_manager.async_engine.echo = False
    return apartments


@router.get("/results")
async def get_apartments(
    page: int = Query(1, ge=1),  # Номер страницы (по умолчанию 1)
    rows_per_page: int = Query(
        100, ge=1
    ),  # Количество строк на странице (по умолчанию 100)
    districts: list[str] | None = Query(None),
    areas: list[str] | None = Query(None),
    addresses: list[str] | None = Query(None),
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    districts_schema = [District(name=d) for d in districts] if districts else None
    areas_schema = [Area(name=a) for a in areas] if areas else None
    addresses_schema = (
        [HouseAddress(address=a) for a in addresses] if addresses else None
    )

    apartments = await new_apart_dao.get_apartments(
        page=page,
        rows_per_page=rows_per_page,
        districts=districts_schema,
        areas=areas_schema,
        addresses=addresses_schema,
    )
    return apartments


@router.get("/results/{apartment_id}", response_model=NewApartSchema)
async def get_apartment_by_id(
    apartment_id: int = Path(..., description="The ID of the apartment to retrieve"),
    new_apart_dao: NewApartDao = Depends(get_new_apart_dao),
):
    apartment = await new_apart_dao.get_apartment_by_id(apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment
