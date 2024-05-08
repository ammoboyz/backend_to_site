from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..student.student import Student
from ..mentor.mentor import Mentor
from .. import Base
from ..base import bigint


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    date_id: Mapped[int] = mapped_column(
        ForeignKey("dates.id")
    )

    first_id: Mapped[bigint] = mapped_column(
        ForeignKey("students.user_id")
    )

    second_id: Mapped[bigint] = mapped_column(
        ForeignKey("mentors.user_id")
    )

    meeting_date: Mapped[datetime] = mapped_column(
        nullable=False
    )

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )

    student: Mapped["Student"] = relationship(
        "Student",
        foreign_keys=[first_id],
        uselist=False,
        backref="meeting_first",
        lazy="selectin"
    )

    mentor: Mapped["Mentor"] = relationship(
        "Mentor",
        foreign_keys=[second_id],
        uselist=False,
        backref="meeting_second",
        lazy="selectin"
    )
