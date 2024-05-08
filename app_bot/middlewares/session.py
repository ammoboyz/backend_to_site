import logging as lg
from typing import Any, Awaitable, Callable, Dict
from contextlib import suppress

from aiogram import BaseMiddleware
from aiogram.types import Update

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)


class SessionMiddleware(BaseMiddleware):
    """
    Middleware for adding session.
    """

    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            async with session.begin():
                session: AsyncSession
                data["session"] = session
                # try:
                await handler(event, data)
                # except (IntegrityError, InvalidRequestError) as e:
                #     await session.rollback()
                #     lg.error(f"Error in SessionMiddleware: {e}")
