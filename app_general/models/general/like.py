from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..mentor.mentor import Mentor
from ..student.student import Student
from .. import Base
from ..base import bigint


class Like(Base):
    __tablename__ = "likes"

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

    message: Mapped[str] = mapped_column(
        default=""
    )

    is_approved: Mapped[bool] = mapped_column(
        default=None,
        nullable=True
    )

    answer: Mapped[str] = mapped_column(
        default=""
    )

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )

    student: Mapped["Student"] = relationship(
        "Student",
        foreign_keys=[first_id],
        uselist=False,
        backref="likes_first",
        lazy="selectin"
    )

    mentor: Mapped["Mentor"] = relationship(
        "Mentor",
        foreign_keys=[second_id],
        uselist=False,
        backref="likes_second",
        lazy="selectin"
    )
