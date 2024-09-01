from sqlalchemy import Integer, String, Column, Numeric, TIMESTAMP, ARRAY, ForeignKey
from database import schema, Base
    
class History(Base):
    __tablename__ = 'history'
    __table_args__ = {'schema': schema}
    
    history_id = Column(Integer, nullable=False, primary_key=True)
    old_house_addresses = Column(ARRAY(String))
    new_house_addresses = Column(ARRAY(String))
    status = Column(String, nullable=False)
