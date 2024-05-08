import os
import asyncio
import logging

from app_bot import middlewares, handlers
from app_bot.database import create_sessionmaker
from app_bot.utils import load_config, func

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage, Redis


log = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger(
        'aiogram.event',
    ).setLevel(logging.WARNING)

    log.info("Starting bot...")
    config = load_config()

    os.environ['TZ'] = config.bot.timezone

    log.info('Set timesone to "%s"' % config.bot.timezone)

    redis: Redis = Redis(host=config.bot.redis)
    storage: RedisStorage = RedisStorage(redis=redis)
    sessionmaker = await create_sessionmaker(config.db)

    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML"
    )
    dp = Dispatcher(storage=storage)

    middlewares.setup(dp, sessionmaker)
    handlers.setup(dp, config)

    bot_info = await bot.me()
    await bot.delete_webhook(drop_pending_updates=True)

    await func.schedule_tasks(bot, sessionmaker)

    router = Router()
    dp.include_router(router)

    try:
        await dp.start_polling(
            bot,
            router=router,
            config=config,
            dp=dp,
            bot_info=bot_info,
            allowed_updates=[
                "message",
                "callback_query",
                "my_chat_member"
            ]
        )
    finally:
        await dp.fsm.storage.close()


try:
    asyncio.run(main())
except (
    KeyboardInterrupt,
    SystemExit,
):
    log.critical("Bot stopped")
