from database import Base, schema
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ARRAY
from pydantic import BaseModel
from datetime import datetime

class OldApart(Base):
    __tablename__ = 'old_apart'
    __table_args__ = {'schema': schema}
    
    old_apart_id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    district = Column(String, nullable = False)
    area = Column(String, nullable = False)
    house_address = Column(String, nullable = False)
    apart_number = Column(String, nullable=False)
    room_count = Column(Integer, nullable=False)
    type_of_settlement = Column(String, nullable=False)
    full_living_area = Column(Numeric, nullable=False)
    total_living_area = Column(Numeric, nullable=False)
    living_area = Column(Numeric, nullable=False)
    members_amount = Column(Integer, nullable=False)
    need = Column(Integer)
    min_floor = Column(Integer, nullable=False)
    max_floor = Column(Integer, nullable=False)
    insert_date = Column(TIMESTAMP, nullable=False)
    list_of_offers = Column(ARRAY(Integer))
    rank = Column(Integer, default=None)
    history_id = Column(Integer, default=None)
    kpu_num = Column(Integer, nullable=False)
    