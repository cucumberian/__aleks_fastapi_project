from pydantic import BaseModel, EmailStr
from database import Base, schema
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema' : schema}
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False)
    hashed_password = Column(String, nullable = False)
    
class SUserRegister(BaseModel):
    email : EmailStr
    hasshed_password : str 
    