from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app_bot.templates.texts import buttons

from .kb_wrapper import kb_wrapper, builder_var


@kb_wrapper
def start(is_student: bool) -> ReplyKeyboardMarkup:
    builder: ReplyKeyboardBuilder = builder_var.get()

    builder.button(text=buttons.VIEW)
    builder.button(text=buttons.PROFILE)
    builder.button(text=buttons.CHANGE_PROFILE)
    if is_student:
        builder.button(text=buttons.FAVOURITE)

    builder.adjust(2)
