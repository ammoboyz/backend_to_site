from typing import Optional
from aiogram.filters.callback_data import CallbackData


class CreatePaymentCallbackFactory(CallbackData, prefix="payment"):
    user_id: int
    pay_code: str
    method_name: str
    days: int = 0
