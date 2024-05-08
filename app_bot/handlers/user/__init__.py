from . import (
    start,
    event,
    register,
    profile,
    start_end,
    favourite
)

from aiogram import Router


def setup(router: Router):
    """
    Register user handlers.

    :param Router router: User Router
    """

    event.register(router)
    register.register(router)
    start.register(router)
    profile.register(router)
    favourite.register(router)
    start_end.register(router)
