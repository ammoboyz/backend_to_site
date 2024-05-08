import datetime
import sys, os

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile, InputMediaPhoto, FSInputFile
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_bot.database.models import User
from app_bot.utils import admin_func
from app_bot.templates.keyboards import admin as admin_kb
from app_bot.templates.texts import admin as admin_text


async def admin_menu(message: Message):
    await message.answer(
        text=admin_text.ADMIN_MENU,
        reply_markup=admin_kb.inline.admin_menu()
    )


async def call_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.set_state()

    await call.message.delete()
    await call.message.answer(
        text=admin_text.ADMIN_MENU,
        reply_markup=admin_kb.inline.admin_menu()
    )


async def stat(call: CallbackQuery, session: AsyncSession, bot: Bot):
    interval = 14
    bot_info = await bot.me()

    image_stats = await admin_func.StatisticsPlotter(
        interval=interval,
        session=session
    ).plot_statistics()

    caption = await admin_func.StatisticString(
        session=session
    ).all_statistics()

    if call.message.photo:
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(
                    image_stats.getvalue(),
                    filename="stats.png"
                ),
                caption=caption,
                parse_mode="HTML"
            ),
            reply_markup=admin_kb.inline.go_back()
        )
    else:
        await call.message.delete()
        await call.message.answer_photo(
            photo=BufferedInputFile(
                image_stats.getvalue(),
                filename="stats.png"
            ),
            caption=caption,
            reply_markup=admin_kb.inline.go_back()
        )


async def download_db(call: CallbackQuery, session: AsyncSession):
    user_list = (await session.scalars(
        select(User.user_id)
    )).all()

    with open("user_ids.txt", "w") as file:
        for user in user_list:
            file.write(str(user) + "\n")
    document = FSInputFile("user_ids.txt")

    await call.message.delete()
    await call.message.answer_document(
        document=document,
        caption=f"<b>📃 Чтобы вернуться в админ панель /admin</b>"
    )


async def restart(call: CallbackQuery):
    await call.message.edit_text(
        text='<b>🔁 Перезапускаю...</b>\n\n'
        '<i>Ожидайте 5 секунд!</i>',
        reply_markup=admin_kb.inline.go_back()
    )
    python = sys.executable
    os.execl(python, python, *sys.argv)


def register(router: Router):
    router.message.register(admin_menu, Command("admin"))
    router.callback_query.register(call_admin_menu, F.data == "admin_menu")
    router.callback_query.register(stat, F.data.startswith("stat_"))
    router.callback_query.register(restart, F.data == "restart")
    router.callback_query.register(download_db, F.data == "download_db")