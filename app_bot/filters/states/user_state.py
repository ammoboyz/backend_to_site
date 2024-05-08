from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    change_full_name = State()
    change_description = State()
    change_pic = State()
    change_position = State()
    change_expertise = State()
    change_course = State()
