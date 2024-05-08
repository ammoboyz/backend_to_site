from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, \
    relationship

from .. import Base
from ..base import bigint


class Date(Base):
    __tablename__ = "dates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[bigint] = mapped_column(
        ForeignKey("mentors.user_id")
    )

    week_day: Mapped[int] = mapped_column(
        nullable=False
    )

    hours: Mapped[int] = mapped_column(
        nullable=False
    )

    minutes: Mapped[int] = mapped_column(
        nullable=False
    )
