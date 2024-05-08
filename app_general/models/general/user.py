from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base
from ..base import bigint


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[bigint] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        default=""
    )

    pic_name: Mapped[str] = mapped_column(
        default=""
    )

    full_name: Mapped[str] = mapped_column(
        default=""
    )

    description: Mapped[str] = mapped_column(
        default=""
    )

    time_zone: Mapped[int] = mapped_column(
        default=0
    )

    where_from: Mapped[str] = mapped_column(
        default=""
    )

    dead: Mapped[bool] = mapped_column(
        default=False
    )

    dead_date: Mapped[date] = mapped_column(
        default=date(1970, 1, 1)
    )

    reg_date: Mapped[date] = mapped_column(
        default=date.today
    )

    is_approved: Mapped[bool] = mapped_column(
        default=False
    )

    def get_pic_url(self, base_url: str) -> str:
        return f"{base_url}photo/{self.pic_name}"
