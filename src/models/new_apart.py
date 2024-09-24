import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from db.database import schema
from models import offer


class NewApart(Base):
    __tablename__ = "new_apart"
    __table_args__ = {"schema": schema}

    new_apart_id: Mapped[int] = mapped_column(primary_key=True)
    district: Mapped[str]
    area: Mapped[str]
    house_address: Mapped[str]
    apart_number: Mapped[int]
    floor: Mapped[int]
    room_count: Mapped[int]
    full_living_area: Mapped[float]
    total_living_area: Mapped[float]
    living_area: Mapped[float]
    status_marker: Mapped[int]
    unique_id: Mapped[int]
    insert_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )
    rank: Mapped[int | None] = mapped_column(default=None)
    history_id: Mapped[int | None] = mapped_column(default=None)

    offers: Mapped[list["offer.Offer"]] = relationship(back_populates="new_apart")
