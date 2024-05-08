import contextvars
import asyncio

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, ReplyKeyboardBuilder
)
from aiogram.types import (
    InlineKeyboardMarkup, ReplyKeyboardMarkup
)


builder_var = contextvars.ContextVar("builder", default=None)


def kb_wrapper(func):
    return_type = func.__annotations__.get('return')

    if return_type is None:
        raise TypeError("Return type is None")

    def get_builder(return_type):
        if return_type == InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
        elif return_type == ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
        else:
            raise TypeError(f"Unsupported return type: {return_type}")

        return builder

    async def async_decorated_function(*args, **kwargs):
        builder = get_builder(return_type)

        builder_var.set(builder)
        await func(*args, **kwargs)

        return builder.as_markup(resize_keyboard=True)

    def sync_decorated_function(*args, **kwargs):
        builder = get_builder(return_type)

        builder_var.set(builder)
        func(*args, **kwargs)

        return builder.as_markup(resize_keyboard=True)

    return (
        async_decorated_function
        if asyncio.iscoroutinefunction(func)
        else sync_decorated_function
    )