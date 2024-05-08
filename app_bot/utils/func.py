import random
import re
import aiocron
import asyncio
import string
import logging as lg
from datetime import datetime, timedelta
from contextlib import suppress
from typing import Union

from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message, CallbackQuery
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)

from app_general.config import Settings

from app_bot.settings import SEND_EXCEPTIONS
from app_bot.templates.keyboards import user as user_kb
from app_bot.templates.texts import user as user_text
from app_bot.database.models import Student, \
    Mentor, User, Meeting


def generate_random_code() -> str:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))


def clean(text: str) -> str:
    result = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', text)
    return result


def days_until(target_date: datetime):
    time_difference = target_date - datetime.now()

    if time_difference.total_seconds() < 0:
        return "нет"
    if time_difference.total_seconds() < 3600:
        return f'{int(time_difference.total_seconds() / 60)} минут'
    elif time_difference.days >= 365:
        years = time_difference.days // 365
        return f'{years} год'
    elif time_difference.days < 1:
        return f'{time_difference.seconds // 3600} часов'
    else:
        return f'{time_difference.days} дней'


async def state_with(chat_id: int, bot: Bot, dp: Dispatcher) -> FSMContext:
    return FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=chat_id,
            user_id=chat_id,
            bot_id=bot.id
        )
    )


def time_format(seconds: int):
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}д {hours}ч и {minutes}м"
    elif hours > 0:
        return f"{hours}ч и {minutes}м"
    elif minutes > 0:
        return f"{minutes}м и {seconds}с"
    else:
        return f"{seconds}с"


def get_path_to_images() -> str:
    # current_path = os.getcwd()
    # parent_path = os.path.dirname(current_path)

    # images_path = os.path.join(
    #     parent_path,
    #     "app_general",
    #     "images"
    # ).replace("\\", "/")

    images_path = "app_general/images"

    return images_path


def get_profile_text(student: Student, mentor: Mentor, user: User) -> str:
    common_data = {
        'full_name': user.full_name,
        'description': user.description or "отсутствует",
    }

    if student:
        finish_text = user_text.PROFILE_STUDENT.format(
            **common_data,
            course=student.course
        )
    else:
        finish_text = user_text.PROFILE_MENTOR.format(
            **common_data,
            position=mentor.position,
            expertise=mentor.expertise,
            time_zone=(
                "+" if user.time_zone > 0 else ""
            ) + str(user.time_zone),
            skills=(
                ', '.join(mentor.skill_list)
            ) if mentor.skill_list else "отсутствуют"
        )

    return finish_text


async def download_pic(
    bot: Bot,
    update: Union[Message, CallbackQuery],
    config: Settings
) -> str:
    path_to_images = get_path_to_images()

    user_profile_photo = await bot.get_user_profile_photos(
        user_id=update.from_user.id
    )

    if isinstance(update, Message):
        if update.photo:
            file_id = update.photo[-1].file_id

        elif update.document:
            file_id = update.document.file_id

        file = await bot.get_file(
            file_id
        )

        await bot.download_file(
            file.file_path,
            f"{path_to_images}/{update.from_user.id}.jpg"
        )

        path = update.from_user.id

    elif user_profile_photo.photos:
        file = await bot.get_file(
            user_profile_photo.photos[0][-1].file_id
        )

        await bot.download_file(
            file.file_path,
            f"{path_to_images}/{update.from_user.id}.jpg"
        )

        path = update.from_user.id
    else:
        path = "main.jpg"

    return str(path)


async def send_reminder(
        bot: Bot,
        sessionmaker: async_sessionmaker
):
    lg.info("send_reminder started")
    now = datetime.now()

    async with sessionmaker() as session:
        async with session.begin():
            session: AsyncSession

            meeting_list = (await session.scalars(
                select(Meeting)
                .where(Meeting.meeting_date <= now)
                .where(
                    Meeting.meeting_date == (
                        now + timedelta(hours=1.5)
                    )
                )
            )).all()

    for meeting in meeting_list:
        if meeting.meeting_date + timedelta(hours=30) == (
            now.replace(second=0)
        ):
            for user in (meeting.student, meeting.mentor):
                with suppress(*SEND_EXCEPTIONS):
                    try:
                        await bot.send_message(
                            chat_id=user.user_id,
                            text=user_text.SEND_REMINDER.format(
                                username=(
                                    meeting.mentor.user.username
                                    if meeting.mentor != user
                                    else meeting.student.user.username
                                ),
                                full_name=(
                                    meeting.mentor.user.full_name
                                    if meeting.mentor != user
                                    else meeting.student.user.full_name
                                ),
                                appoint_date=meeting.meeting_date.strftime('%d.%m.%Y %H:%M'),
                                time=now.minute - meeting.meeting_date.minute
                            ),
                            disable_web_page_preview=True
                        )
                    except TelegramRetryAfter as e:
                        await asyncio.sleep(e.retry_after)

        elif meeting.meeting_date == (
            now.replace(minute=0)
        ):
            for user in (meeting.student, meeting.mentor):
                with suppress(*SEND_EXCEPTIONS):
                    try:
                        await bot.send_message(
                            chat_id=user.user_id,
                            text=user_text.CONSULTATION_STARTED.format(
                                username=(
                                    meeting.mentor.user.username
                                    if meeting.mentor != user
                                    else meeting.student.user.username
                                ),
                                full_name=(
                                    meeting.mentor.user.full_name
                                    if meeting.mentor != user
                                    else meeting.student.user.full_name
                                ),
                                appoint_date=meeting.meeting_date.strftime('%d.%m.%Y %H:%M'),
                            ),
                            disable_web_page_preview=True
                        )
                    except TelegramRetryAfter as e:
                        await asyncio.sleep(e.retry_after)

        elif meeting.meeting_date == (
            now + timedelta(hours=1)
        ).replace(second=0):
            with suppress(*SEND_EXCEPTIONS):
                try:
                    await bot.send_message(
                        chat_id=meeting.student.user_id,
                        text=user_text.CONSULTATION_ENDED.format(
                            username=meeting.mentor.user.username,
                            full_name=meeting.mentor.user.full_name
                        ),
                        disable_web_page_preview=True,
                        reply_markup=user_kb.inline.send_feedback(
                            meeting.mentor.user_id
                        )
                    )
                except TelegramRetryAfter as e:
                    await asyncio.sleep(e.retry_after)



async def schedule_tasks(
    bot: Bot,
    sessionmaker: async_sessionmaker
):
    aiocron.crontab(
        "*/1 * * * *",
        send_reminder,
        (bot, sessionmaker)
    )
