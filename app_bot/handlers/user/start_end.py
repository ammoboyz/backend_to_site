from aiogram import Router

from .start import start


def register(router: Router):
    router.message.register(start)