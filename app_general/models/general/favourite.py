from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..mentor.mentor import Mentor
from .. import Base
from ..base import bigint


class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    first_id: Mapped[bigint] = mapped_column(
        ForeignKey("students.user_id")
    )

    second_id: Mapped[bigint] = mapped_column(
        ForeignKey("mentors.user_id")
    )

    mentor: Mapped["Mentor"] = relationship(
        "Mentor",
        foreign_keys=[second_id],
        uselist=False,
        backref="favourite_second",
        lazy="selectin"
    )

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )
