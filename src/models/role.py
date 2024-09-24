from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY
from sqlalchemy.types import INTEGER

from db.database import Base
from db.database import schema

from models import user

class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": schema}

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(nullable=False)
    duties: Mapped[list[int]] = mapped_column(
        ARRAY(INTEGER),
        nullable=False,
    )
    users: Mapped[list["user.UserOrm"]] = relationship(back_populates="role")

    class from_attributes:
        orm_mode = True
