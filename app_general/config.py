# import json

from pydantic_settings import BaseSettings


class DB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class Bot(BaseSettings):
    token: str
    redis: str
    webapp_url: str
    timezone: str
    admins: list[int]
    manager: str


class Api(BaseSettings):
    url: str
    webapp_url: str
    time_zone: str


class Settings(BaseSettings):
    api: Api
    db: DB
    bot: Bot

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


def load_config(env_file=".env") -> Settings:
    """
    Loads .env file into BaseSettings

    :param str env_file: Env file, defaults to ".env"
    :return Settings: Settings object
    """

    settings = Settings(_env_file=env_file)
    return settings
