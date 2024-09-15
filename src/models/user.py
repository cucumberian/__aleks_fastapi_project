from pydantic import BaseModel, EmailStr
from db.database import Base, schema
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import Optional

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema' : schema}
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False)
    hashed_password = Column(String, nullable = False)
    role_id = Column(Integer, ForeignKey(f"{schema}.role.role_id"))
    name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    avaliable_aparts = "with unnest(apart where user_id = 1)"
    class from_attributes:
        orm_mode = True
    
class SUserAuth(BaseModel):
    email : EmailStr
    hashed_password : str 
    
class UserResponse(BaseModel):
    user_id: int
    role_id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    email: str
    last_name: Optional[str]