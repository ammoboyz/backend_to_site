from fastapi import Request
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage, Redis

from app_api.utils import Settings


class BotMiddleware:
    def __init__(
            self,
            config: Settings
    ) -> None:
        self.config = config
        redis = Redis(host=config.bot.redis)
        self.storage = RedisStorage(redis=redis)
        self.dp = Dispatcher(storage=self.storage)
        # self.bot = Bot(config.bot.token)
        # self.dp = Dispatcher(storage=storage)

    async def __call__(self, request: Request, call_next):
        request.state.bot = Bot(
            self.config.bot.token,
            parse_mode="HTML"
        )
        request.state.dp = self.dp

        try:
            response = await call_next(request)
        finally:
            await request.state.bot.session.close()

        return response
