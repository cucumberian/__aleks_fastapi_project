from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import String
from sqlalchemy.types import ARRAY

from db.database import schema, Base


class History(Base):
    __tablename__ = "history"
    __table_args__ = {"schema": schema}

    history_id: Mapped[int] = mapped_column(primary_key=True)
    old_house_addresses: Mapped[list[str]] = mapped_column(
        ARRAY(String),
    )
    new_house_addresses: Mapped[list[str]] = mapped_column(
        ARRAY(String),
    )
    status: Mapped[str]

    class from_attributes:
        orm_mode = True
