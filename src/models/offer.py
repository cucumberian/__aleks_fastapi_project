from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Relationship
from db.database import schema, Base

class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = {"schema": schema}

    offer_id = Column(Integer, nullable=False, primary_key=True)
    old_apart_id = Column(ForeignKey(f"{schema}.old_apart.old_apart_id"))  # Correct
    new_apart_id = Column(ForeignKey(f"{schema}.new_apart.new_apart_id"))  # Correct
    status = Column(String, nullable=False, default="Подбор на рассмотрении")
    insert_date = Column(TIMESTAMP, nullable=False)
    
    class from_attributes:
        orm_mode = True