from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base
from ..base import bigint


class Dislike(Base):
    __tablename__ = "dislikes"

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

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )
