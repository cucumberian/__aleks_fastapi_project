from datetime import datetime
from pydantic import BaseModel


class NewApartSchema(BaseModel):
    new_apart_id: int
    district: list[str] | None = None
    area: list[str] | None = None
    house_address: list[str] | None = None
    apart_number: int
    floor: int
    room_count: int
    full_living_area: float
    total_living_are: float
    living_area: float
    status_marker: int
    unique_id: int
    insert_date: datetime
    rank: int
    history_id: int

    class from_attributes:
        orm_mode = True
