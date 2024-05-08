from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base
from ..base import bigint


class Feedback(Base):
    __tablename__ = "feedbacks"

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

    description: Mapped[str] = mapped_column(
        default=""
    )

    score: Mapped[int] = mapped_column(
        default=0
    )

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )
