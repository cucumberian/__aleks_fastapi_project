from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base, schema
from models import role


class UserOrm(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": schema}

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            column=f"{schema}.role.role_id",
            ondelete="SET NULL",
        ),
        default=None,
    )
    role: Mapped["role.Role"] = relationship(back_populates="users")
    name: Mapped[str | None]
    surname: Mapped[str | None]
    last_name: Mapped[str | None]
    # avaliable_aparts = "with unnest(apart where user_id = 1)"
