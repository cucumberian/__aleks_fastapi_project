import datetime

from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import Base
from db.database import schema


class CannotOffer(Base):
    __tablename__ = "cannot_offer"
    __table_args__ = {"schema": schema}

    cannot_offer_id: Mapped[int] = mapped_column(primary_key=True)
    old_apart_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f"{schema}.old_apart.old_apart_id",
        )
    )
    insert_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )
    status: Mapped[str] = mapped_column(
        nullable=False,
        default="Подбор на рассмотрении",
    )

    class from_attributes:
        orm_mode = True
