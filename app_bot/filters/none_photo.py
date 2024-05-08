from app_general.config import Settings
from app_bot.database.models import User

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class NonePhotoFilter(Filter):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
            self,
            update: Message | CallbackQuery,
            user: User
        ) -> bool:

        return not bool(user.pic_name)
