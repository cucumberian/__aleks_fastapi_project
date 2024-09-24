import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base, schema
from models import offer


class OldApart(Base):
    __tablename__ = "old_apart"
    __table_args__ = {"schema": schema}

    old_apart_id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str]
    district: Mapped[str]
    area: Mapped[str]
    house_address: Mapped[str]
    apart_number: Mapped[int]
    room_count: Mapped[int]
    type_of_settlement: Mapped[str]
    full_living_area: Mapped[float]
    total_living_area: Mapped[float]
    living_area: Mapped[float]
    members_amount: Mapped[int]
    need: Mapped[int]  # or Mapped[int | None] = None
    min_floor: Mapped[int]
    max_floor: Mapped[int]
    insert_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )
    # deleted list_of_offers т.к. он уже существует в ORM связи offers
    # list_of_offers: Mapped[list[int]] = mapped_column(
    #     ARRAY(INTEGER),
    # )
    rank: Mapped[int | None] = mapped_column(default=None)
    history_id: Mapped[int | None] = mapped_column(default=None)
    kpu_num: Mapped[int]
    offers: Mapped[list["offer.Offer"]] = relationship(back_populates="old_apart")

    class from_attributes:
        orm_mode = True
