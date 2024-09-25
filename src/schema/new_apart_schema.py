import datetime
from pydantic import BaseModel
from pydantic import Field
# from schema.offer_schama import OfferSchema

class NewApartSchema(BaseModel):
    new_apart_id: int
    district: str
    area: str
    house_address: str
    apart_number: int = Field(ge=0)
    floor: int
    room_count: int = Field(ge=0)
    full_living_area: float = Field(ge=0)
    total_living_area: float = Field(ge=0)
    living_area: float = Field(ge=0)
    status_marker: int
    unique_id: int
    insert_date: datetime.datetime
    rank: int | None = None
    history_id: int | None = None

# class NewApartSchemaRelOffers(NewApartSchema):
#     offers: list[OfferSchema]
