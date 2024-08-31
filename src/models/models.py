from sqlalchemy import Integer, String, Column, Numeric, TIMESTAMP, ARRAY, ForeignKey
from src.database import schema, Base

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

class Offer(Base):
    __tablename__ = 'offer'
    __table_args__ = {'schema': schema}
    
    offer_id = Column(Integer, nullable=False, primary_key=True)
    old_apart_id = Column(ForeignKey(f'{schema}.old_apart.old_apart_id'))
    new_apart_id = Column(ForeignKey(f'{schema}.new_apart.new_apart_id'))
    status = Column(String, nullable=False, default='Подбор на расммотрении')
    insert_date = Column(TIMESTAMP, nullable=False)
    
class CannotOffer(Base):
    __tablename__ = 'cannot_offer'
    __table_args__ = {'schema': schema}
    
    cannot_offer_id = Column(Integer, nullable=False, primary_key=True)
    old_apart_id = Column(ForeignKey(f'{schema}.old_apart.old_apart_id'))
    insert_date = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False, default='Подбор на расммотрении')
    
class History(Base):
    __tablename__ = 'history'
    __table_args__ = {'schema': schema}
    
    history_id = Column(Integer, nullable=False, primary_key=True)
    old_house_addresses = Column(ARRAY(String))
    new_house_addresses = Column(ARRAY(String))
    status = Column(String, nullable=False)

