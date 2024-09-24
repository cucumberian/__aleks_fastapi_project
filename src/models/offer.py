import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from db.database import schema, Base
from models import old_apart
from models import new_apart


class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = {"schema": schema}

    offer_id: Mapped[int] = mapped_column(primary_key=True)

    old_apart_id: Mapped[int] = mapped_column(
        ForeignKey(column=f"{schema}.old_apart.old_apart_id", ondelete="CASCADE")
    )
    old_apart: Mapped["old_apart.OldApart"] = relationship(back_populates="offers")

    new_apart_id: Mapped[int] = mapped_column(
        ForeignKey(column=f"{schema}.new_apart.new_apart_id", ondelete="CASCADE")
    )
    new_apart: Mapped["new_apart.NewApart"] = relationship(back_populates="offers")

    status: Mapped[str] = mapped_column(default="Подбор на рассмотрении")
    insert_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )

    class from_attributes:
        orm_mode = True
