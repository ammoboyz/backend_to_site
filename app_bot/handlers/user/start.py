from contextlib import suppress
from typing import Union

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, or_f, Command
from aiogram.exceptions import TelegramRetryAfter

from app_bot.database.models import Student
from app_bot.utils import Settings
from app_bot.templates.texts import buttons, user as user_text
from app_bot.templates.keyboards import user as user_kb
from app_bot.templates.texts.commands import START_COMMANDS


async def start(
        update: Union[Message, CallbackQuery],
        student: Student,
        bot: Bot
):
    with suppress(TelegramRetryAfter):
        await bot.set_my_commands(START_COMMANDS)

    await bot.send_message(
        chat_id=update.from_user.id,
        text=user_text.START,
        reply_markup=user_kb.reply.start(bool(student)),
        disable_web_page_preview=True
    )


async def view(
        message: Message,
        config: Settings
):
    await message.answer(
        text=user_text.VIEW,
        reply_markup=user_kb.inline.webapp(config)
    )


def register(router: Router):
    router.message.register(start, CommandStart())
    router.message.register(
        view,
        or_f(
            Command("view"),
            F.text == buttons.VIEW
        )
    )
