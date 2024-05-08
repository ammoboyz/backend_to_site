from .config import ConfigMiddleware
from .bot import BotMiddleware
from .webapp import WebAppMiddleware

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app_api.utils import Settings


def setup(app: FastAPI, config: Settings):
    """
    Initializes and binds all the middlewares.

    :param FastAPI app: The FastAPI instance.
    :param Settings config: The configuration settings.
    """

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=ConfigMiddleware(config)
    )

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=BotMiddleware(config)
    )

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=WebAppMiddleware(config)
    )
