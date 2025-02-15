from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from db.database import schema, Base


class CannotOffer(Base):
    __tablename__ = "cannot_offer"
    __table_args__ = {"schema": schema}

    cannot_offer_id = Column(Integer, nullable=False, primary_key=True)
    old_apart_id = Column(ForeignKey(f"{schema}.old_apart.old_apart_id"))
    insert_date = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False, default="Подбор на рассмотрении")

    class from_attributes:
        orm_mode = True
