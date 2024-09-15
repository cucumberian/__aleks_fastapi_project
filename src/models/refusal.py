from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from db.database import schema

class Refusal(Base):
    __tablename__ = "refusal"
    __table_args__ = {"schema": schema}

    refusal_id = Column(Integer, nullable=False, primary_key=True)

    class from_attributes:
        orm_mode = True
