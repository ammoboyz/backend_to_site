from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .. import Base


class WhiteList(Base):
    __tablename__ = "white_list"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        default=""
    )

    full_name: Mapped[str] = mapped_column(
        default=""
    )

    is_student: Mapped[bool] = mapped_column(
        default=""
    )

    position: Mapped[str] = mapped_column(
        default=""
    )

    competence: Mapped[str] = mapped_column(
        default=""
    )

    time_zone: Mapped[int] = mapped_column(
        default=3
    )

    skills: Mapped[str] = mapped_column(
        default=""
    )

    course: Mapped[int] = mapped_column(
        default=0
    )

    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now
    )
