from pydantic import BaseModel


class FilterSchema(BaseModel):
    district: list[str] | None = None
    area: list[str] | None = None
    house_address: list[str] | None = None
