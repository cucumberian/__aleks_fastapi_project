from pydantic import BaseModel

class HouseAddress(BaseModel):
    address: str