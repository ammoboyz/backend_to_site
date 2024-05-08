from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app_general.models import Student


class IsStudentFilter(Filter):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
            self,
            update: Message | CallbackQuery,
            student: Student
    ) -> bool:
        return bool(student)
