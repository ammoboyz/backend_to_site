import time
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery


class AntiFloodMiddleware(BaseMiddleware):
    timedelta_limiter: int = 0.4

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state: FSMContext = data['state']
        fsm_data = await state.get_data()
        send_timeout = fsm_data.get('send_timeout', 0)

        if isinstance(event, (Message, CallbackQuery)):
            if (time.time() - send_timeout) < self.timedelta_limiter:
                return

            await state.update_data(
                send_timeout=time.time()
            )

            return await handler(event, data)
