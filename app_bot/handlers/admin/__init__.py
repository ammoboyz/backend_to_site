from . import (
    menu,
    mailling,
    link,
    # subscribe,
    commands,
    white_list
)

from app_bot.utils import Settings
from app_bot.filters import IsAdmin
from aiogram import Router


def setup(router: Router, config: Settings):
    """
    Register user handlers.

    :param Dispatcher dp: Dispatcher (root Router), needed for events
    :param Router router: User Router
    """

    router.message.filter(IsAdmin())
    router.callback_query.filter(IsAdmin())

    commands.register(router)
    # subscribe.register(router)
    menu.register(router)
    mailling.register(router)
    link.register(router)
    white_list.register(router)
