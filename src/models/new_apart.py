from database import Base, schema
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP

class NewApart(Base):
    __tablename__ = 'new_apart'
    __table_args__ = {'schema': schema}
    
    new_apart_id = Column(Integer, primary_key=True)
    district = Column(String, nullable = False)
    area = Column(String, nullable = False) 
    house_address = Column(String, nullable = False)
    apart_number = Column(String, nullable=False)
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