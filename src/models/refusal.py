from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import schema
from db.database import Base


class Refusal(Base):
    __tablename__ = "refusal"
    __table_args__ = {"schema": schema}

    refusal_id: Mapped[int] = mapped_column(primary_key=True)

    class from_attributes:
        orm_mode = True
