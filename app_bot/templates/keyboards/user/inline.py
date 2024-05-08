from typing import List

from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, \
    WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_widgets.pagination import KeyboardPaginator

from app_general.config import Settings
from app_bot.settings import SKILLS_DEFAULT_LIST
from app_general.models import Favourite

from .kb_wrapper import kb_wrapper, builder_var


@kb_wrapper
def webapp(config: Settings) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="Открыть CodeMates",
        web_app=WebAppInfo(
            url=config.api.webapp_url
        )
    )


@kb_wrapper
def captcha() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="✨ Начать",
        callback_data="captcha"
    )


@kb_wrapper
def none_photo() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="⏭ Пропустить",
        callback_data="none_photo:skip"
    )


@kb_wrapper
def profile() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="🛠 Изменить профиль",
        callback_data="change_profile"
    )


@kb_wrapper
def back_to_profile() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="◀️ Вернуться назад",
        callback_data="change_profile"
    )


@kb_wrapper
def change_profile(is_student: bool) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()


    builder.button(
        text="Изменить полное имя",
        callback_data="change_profile:full_name"
    )

    builder.button(
        text="Изменить описание профиля",
        callback_data="change_profile:description"
    )

    builder.button(
        text="Изменить фото профиля",
        callback_data="change_profile:pic"
    )

    if not is_student:
        builder.button(
            text="Изменить должность",
            callback_data="change_profile:position"
        )

        builder.button(
            text="Изменить сферы компетенций",
            callback_data="change_profile:skill"
        )

        builder.button(
            text="Изменить экспертизу",
            callback_data="change_profile:expertise"
        )

        builder.button(
            text="Изменить часовой пояс",
            callback_data="change_profile:time_zone"
        )

    builder.adjust(1)


@kb_wrapper
def change_skill(skill_list: list[str]) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    i = 0
    adjust_list = []
    for skill in SKILLS_DEFAULT_LIST:
        i += 1

        if i%2 == 0:
            adjust_list.append(2)

        builder.button(
            text=skill + (
                " ✅" if skill in skill_list else ""
            ),
            callback_data=f"input_skill:{skill}"
        )

    builder.button(
        text="◀️ Вернуться назад",
        callback_data="change_profile"
    )

    builder.adjust(1)


@kb_wrapper
def change_pic() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="⏭ Использовать фото из Телеграм",
        callback_data="change_pic:skip"
    )

    builder.button(
        text="◀️ Вернуться назад",
        callback_data="change_profile"
    )

    builder.adjust(1)


@kb_wrapper
def change_time_zone() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    for i in range(-12, 13):
        builder.button(
            text=f"GMT {'+' if i > 0 else ''}{i}",
            callback_data=f"input_time_zone:{i}"
        )

    builder.button(
        text="◀️ Вернуться назад",
        callback_data="change_profile"
    )

    builder.adjust(4, 4, 4, 4, 4, 4, 1, 1)


@kb_wrapper
def change_course() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    for i in range(1, 3):
        builder.button(
            text=f"Курс {i}",
            callback_data=f"button_{i}"
        )

    builder.adjust(2)


@kb_wrapper
def meeting_contact(username: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="✉️ Контакт",
        url=f"https://t.me/{username}"
    )


@kb_wrapper
def send_feedback(user_id: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    for i in range(1, 6):
        builder.button(
            text=str(i),
            callback_data=f"send_feedback:{user_id}:{i}"
        )

    builder.adjust(5)


@kb_wrapper
def favourite_menu(
    favourite_list: List[Favourite],
    router: Router
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    if not favourite_list:
        return builder.button(
            text="😞 Тут пока пусто",
            callback_data="pass"
        )

    for favourite in favourite_list:
        builder.button(
            text=favourite.mentor.user.full_name,
            callback_data=f"favourite_mentor:{favourite.second_id}"
        )

    return KeyboardPaginator(
        data=builder.buttons,
        router=router
    )


@kb_wrapper
def favourite_mentor(mentor_id: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="🚮 Удалить из избранных",
        callback_data=f"favourite_approve:{mentor_id}"
    )

    builder.button(
        text="◀️ Назад",
        callback_data=f"favourite_menu"
    )


@kb_wrapper
def favourite_approve(mentor_id: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text=f"🚮 Удалить",
        callback_data=f"favourite_delete:{mentor_id}"
    )

    builder.button(
        text="◀️ Назад",
        callback_data=f"favourite_mentor:{mentor_id}"
    )


@kb_wrapper
def favourite_delete() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = builder_var.get()

    builder.button(
        text="◀️ Вернуться назад",
        callback_data=f"favourite_menu"
    )