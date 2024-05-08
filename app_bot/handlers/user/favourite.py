from typing import Union

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, \
    InputMediaPhoto, BufferedInputFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app_bot.filters import IsStudentFilter
from app_bot.utils import services
from app_bot.templates.texts import buttons, user as user_text
from app_bot.templates.keyboards import user as user_kb
from app_bot.database.models import Mentor, Student, Favourite


async def favourite_menu(
        update: Union[Message, CallbackQuery],
        router: Router,
        student: Student
):
    if isinstance(update, Message):
        await update.answer_photo(
            photo="https://telegra.ph/file/30b4e01e86b6673de3601.png",
            caption=user_text.FAVOURITE_MENU,
            reply_markup=user_kb.inline.favourite_menu(
                favourite_list=student.favourites,
                router=router
            )
        )

    elif isinstance(update, CallbackQuery):
        await update.message.edit_media(
            media=InputMediaPhoto(
                media="https://telegra.ph/file/30b4e01e86b6673de3601.png",
                caption=user_text.FAVOURITE_MENU,
                parse_mode="HTML"
            ),
            reply_markup=user_kb.inline.favourite_menu(
                favourite_list=student.favourites,
                router=router
            )
        )


async def favourite_mentor(
        call: CallbackQuery,
        session: AsyncSession,
        student: Student
):
    mentor_id = int(call.data.split(":")[-1])

    mentor = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == mentor_id)
    )

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=BufferedInputFile(
                await services.get_photo(mentor.user.pic_name),
                "image.jpg"
            ),
            caption=user_text.FAVOURITE_MENTOR.format(
                username=mentor.user.username,
                full_name=mentor.user.full_name,
                description=mentor.user.description,
                position=mentor.position,
                skills=', '.join(mentor.skill_list),
                expertise=mentor.expertise,
                time_zone=mentor.user.time_zone
            ),
            parse_mode="HTML"
        ),
        reply_markup=user_kb.inline.favourite_mentor(mentor_id)
    )


async def favourite_approve(
        call: CallbackQuery,
        session: AsyncSession
):
    mentor_id = int(call.data.split(":")[-1])

    mentor = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == mentor_id)
    )

    await call.message.edit_caption(
        caption=user_text.FAVOURITE_APPROVE_DELETE.format(
            username=mentor.user.username,
            full_name=mentor.user.full_name
        ),
        reply_markup=user_kb.inline.favourite_approve(mentor_id)
    )


async def favourite_delete(
        call: CallbackQuery,
        session: AsyncSession
):
    mentor_id = int(call.data.split(":")[-1])

    mentor = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == mentor_id)
    )

    await session.execute(
        delete(Favourite)
        .where(Favourite.first_id == call.from_user.id)
        .where(Favourite.second_id == mentor_id)
    )

    await call.message.edit_caption(
        caption=user_text.FAVOURITE_DELETE(
            username=mentor.user.username,
            full_name=mentor.user.full_name
        ),
        reply_markup=user_kb.inline.favourite_delete()
    )


def register(router: Router):
    router.message.register(favourite_menu, F.text == buttons.FAVOURITE, IsStudentFilter())
    router.callback_query.register(favourite_menu, F.data == "favourite_menu")
    router.callback_query.register(favourite_mentor, F.data.startswith("favourite_mentor:"))

    router.callback_query.register(favourite_approve, F.data.startswith("favourite_approve:"))
    router.callback_query.register(favourite_delete, F.data.startswith("favourite_delete:"))
