from database import Base, schema
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NewApart(Base):
    __tablename__ = 'new_apart'
    __table_args__ = {'schema': schema}
    
    new_apart_id = Column(Integer, primary_key=True)
    district = Column(String, nullable = False)
    area = Column(String, nullable = False) 
    house_address = Column(String, nullable = False)
    apart_number = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    room_count = Column(Integer, nullable=False)
    full_living_area = Column(Numeric, nullable=False)
    total_living_area = Column(Numeric, nullable=False)
    living_area = Column(Numeric, nullable=False)
    status_marker = Column(Integer, nullable=False)
    unique_id = Column(Integer, nullable=False)
    insert_date = Column(TIMESTAMP, nullable=False)
    rank = Column(Integer, default=None)
    history_id = Column(Integer, default=None)
    
class SNewApart(BaseModel):
    new_apart_id : int
    district :  Optional[List[str] | None] = None
    area : Optional[List[str] | None] = None
    house_address : Optional[List[str] | None] = None
    apart_number : int
    floor : int
    room_count : int
    full_living_area : float
    total_living_are : float
    living_area : float
    status_marker : int
    unique_id : int
    insert_date : datetime
    rank : int
    history_id : int
    
    class from_attributes:
        orm_mode = True
        
        