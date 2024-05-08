from aiogram.types import BotCommand


START_COMMANDS = [
    BotCommand(
        command="/start",
        description="Перезапуск"
    ),
    BotCommand(
        command="/watch",
        description="Начать листать ленты"
    ),
    BotCommand(
        command="/profile",
        description="Мой профиль"
    ),
    BotCommand(
        command="/edit",
        description="Изменить анкету"
    )
]
