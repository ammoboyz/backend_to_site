import os
from fastapi import FastAPI

from app_api import handlers, middlewares
from app_api.utils import load_config


config = load_config()
os.environ['TZ'] = config.api.time_zone
app = FastAPI()

handlers.setup(app, config)
middlewares.setup(app, config)
