from typing import Any, Awaitable, Callable, Dict, Optional
from contextlib import suppress

from aiogram import BaseMiddleware, types, Bot
from aiogram.types import Update

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app_bot.utils import Settings
from app_bot.database.models import WhiteList
from app_bot.templates.texts import user as user_text
from app_bot.settings import SEND_EXCEPTIONS


class NotEnterMiddleware(BaseMiddleware):
    """
    Middleware for captcha.
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        event_user: Optional[types.User] = data.get("event_from_user")
        session: AsyncSession = data['session']
        bot: Bot = data['bot']
        config: Settings = data['config']

        white_list = (await session.scalars(
            select(WhiteList.username)
        )).all()

        if event_user.username not in white_list:
            with suppress(*SEND_EXCEPTIONS):
                return await bot.send_message(
                    chat_id=event_user.id,
                    text=user_text.NOT_ENTER.format(
                        config.bot.manager
                    )
                )

        return await handler(event, data)
