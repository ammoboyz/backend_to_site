from typing import List

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .. import Base
from .skill import Skill
from .date import Date
from ..general.feedback import Feedback
from ..general.user import User
from ..base import bigint


class Mentor(Base):
    __tablename__ = "mentors"

    user_id: Mapped[bigint] = mapped_column(
        ForeignKey(User.user_id),
        primary_key=True
    )

    position: Mapped[str] = mapped_column(
        default=""
    )

    expertise: Mapped[str] = mapped_column(
        default=""
    )

    cons_type: Mapped[str] = mapped_column(
        default=""
    )

    reg_date: Mapped[date] = mapped_column(
        default=date.today
    )

    limit_in_week: Mapped[int] = mapped_column(
        default=0
    )

    user: Mapped["User"] = relationship(
        "User",
        backref="mentor",
        uselist=False,
        lazy="selectin"
    )

    skills: Mapped[List["Skill"]] = relationship(
        "Skill",
        backref="mentor",
        uselist=True,
        lazy="selectin"
    )

    feedbacks: Mapped[List["Feedback"]] = relationship(
        "Feedback",
        backref="mentor",
        uselist=True,
        lazy="selectin"
    )

    dates: Mapped[List["Date"]] = relationship(
        "Date",
        backref="mentor",
        uselist=True,
        lazy="selectin"
    )

    @property
    def skill_list(self) -> list[str]:
        result_list = []

        for skill in self.skills:
            result_list.append(skill.skill)

        return result_list
