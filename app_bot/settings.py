from aiogram.exceptions import (
    TelegramForbiddenError,
    TelegramBadRequest,
    TelegramAPIError,
    TelegramRetryAfter
)


SEND_EXCEPTIONS = [
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError
]


SKILLS_DEFAULT_LIST = [
    "SaaS",
    "E-commerce",
    "Entrepreneurship",
    "Marketplaces",
    "Investor relations",
    "Retail",
    "Карьерные консультации",
    "Бизнес аналитика",
    "AB - тестирование",
    "Product management",
    "MLOps",
    "Большие данные",
    "Data-Driven Science",
    "Computer Vision",
    "Генеративные модели",
    "Backend",
    "DevOps",
    "NLP",
    "EdTech",
    "RecSys",
    "Frontend"
]
