from typing import List

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .. import Base
from .interest import Ineterest
from ..general.favourite import Favourite
from ..general.user import User
from ..base import bigint


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[bigint] = mapped_column(
        ForeignKey(User.user_id),
        primary_key=True
    )

    reg_date: Mapped[date] = mapped_column(
        default=date.today
    )

    user: Mapped[User] = relationship(
        "User",
        backref="student",
        uselist=False,
        lazy="selectin"
    )

    course: Mapped[int] = mapped_column(
        default=0
    )

    favourites: Mapped[List["Favourite"]] = relationship(
        "Favourite",
        backref="student",
        uselist=True,
        lazy="selectin"
    )
