from pydantic import BaseModel
from typing import List, Optional

class SfilterSchema(BaseModel):
    district: Optional[List[str]] = None
    area: Optional[List[str]] = None
    house_address: Optional[List[str]] = None
