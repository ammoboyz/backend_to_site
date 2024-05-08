from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base
from ..base import bigint


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[bigint] = mapped_column(
        ForeignKey("mentors.user_id")
    )

    skill: Mapped[str] = mapped_column(
        default=""
    )
