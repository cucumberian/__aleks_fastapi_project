from sqlalchemy import Index, Integer, String, Column, ForeignKey, ARRAY
from db.database import schema, Base

class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema' : schema}
    
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)
    duties = Column(ARRAY(String))
    
    class from_attributes:
        orm_mode = True