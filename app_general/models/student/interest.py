from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base
from ..base import bigint


class Ineterest(Base):
    __tablename__ = "interests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[bigint] = mapped_column(
        ForeignKey("students.user_id")
    )

    interest: Mapped[str] = mapped_column(
        default=""
    )
