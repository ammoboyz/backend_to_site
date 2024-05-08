from typing import Union

from aiogram import F, Router, Bot
from aiogram.filters import or_f
from aiogram.types import Message, CallbackQuery

from app_bot.filters import NonePhotoFilter
from app_bot.utils import func, Settings
from app_bot.templates.texts import user as user_text
from app_bot.templates.keyboards import user as user_kb
from app_bot.database.models import User, Student

from .start import start


async def none_photo(
        update: Union[CallbackQuery, Message],
        student: Student,
        bot: Bot
):
    await bot.send_message(
        chat_id=update.from_user.id,
        text=user_text.NONE_PHOTO,
        reply_markup=user_kb.inline.none_photo()
    )


async def none_photo_skip(
        call: CallbackQuery,
        config: Settings,
        student: Student,
        bot: Bot,
        user: User
):
    pic_url = await func.download_pic(bot, call, config)

    user.pic_name = pic_url

    await call.message.edit_text(
        text=user_text.PHOTO_DONE
    )

    return await start(call, student, bot)


async def none_photo_input(
        message: Message,
        bot: Bot,
        config: Settings,
        student: Student,
        user: User
):
    if message.document:
        file_name = message.document.file_name
        file_extension = file_name.split('.')[-1].lower()

        if file_extension != "jpg":
            return await message.reply(
                text=user_text.PHOTO_ERROR,
                reply_markup=user_kb.inline.back_to_profile()
            )

    pic_url = await func.download_pic(bot, message, config)
    user.pic_name = pic_url

    await message.answer(
        text=user_text.PHOTO_DONE
    )

    return await start(message, student, bot)


def register(router: Router):
    router.callback_query.register(
        none_photo_skip,
        F.data == "none_photo:skip",
        NonePhotoFilter()
    )
    router.message.register(
        none_photo_input,
        or_f(F.document, F.photo),
        NonePhotoFilter()
    )

    router.callback_query.register(
        none_photo,
        NonePhotoFilter()
    )
    router.message.register(
        none_photo,
        NonePhotoFilter()
    )
