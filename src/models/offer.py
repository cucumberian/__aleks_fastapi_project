from sqlalchemy import Integer, String, Column, Numeric, TIMESTAMP, ARRAY, ForeignKey
from database import schema, Base

class Offer(Base):
    __tablename__ = 'offer'
    __table_args__ = {'schema': schema}
    
    offer_id = Column(Integer, nullable=False, primary_key=True)
    old_apart_id = Column(ForeignKey(f'{schema}.old_apart.old_apart_id'))
    new_apart_id = Column(ForeignKey(f'{schema}.new_apart.new_apart_id'))
    status = Column(String, nullable=False, default='Подбор на расммотрении')
    insert_date = Column(TIMESTAMP, nullable=False)