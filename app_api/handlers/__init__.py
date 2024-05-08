from . import (
    swipe,
    profile,
    like,
    meeting,
    date,
    photo,
    notification
)

from app_api.utils import Settings
from fastapi import FastAPI


def setup(app: FastAPI, config: Settings):
    """
    Set up all the handlers and routers, and bind filters.

    :param FastAPI app: The FastAPI instance.
    :param Settings config: The configuration settings.
    """

    notification.register(app)
    photo.register(app)
    swipe.register(app)
    profile.register(app)
    like.register(app)
    meeting.register(app)
    date.register(app)
