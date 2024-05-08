from typing import Union
from datetime import datetime, timedelta

from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_api.database.models import Student, Mentor, User


async def state_with(
        user_id: int,
        bot: Bot,
        dp: Dispatcher
) -> FSMContext:
    return FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=user_id,
            user_id=user_id,
            bot_id=bot.id
        )
    )


async def check_user(
        user_id: int,
        model: Union[User, Mentor, Student],
        session: AsyncSession
) -> bool:
    return bool(await session.scalar(
        select(model)
        .where(model.user_id == user_id)
    ))


def next_weekday(week_day: int, hour: int, minute: int) -> datetime:
    current_datetime = datetime.now()

    days_until_target = (
        week_day - current_datetime.weekday() + 7
    ) % 7

    next_target_date = current_datetime + timedelta(
        days=days_until_target
    )

    if next_target_date <= current_datetime:
        next_target_date += timedelta(days=7)

    next_target_date = next_target_date.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0
    )

    return next_target_date
