from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    mail = State()

    link_add = State()
    link_delete = State()

    sub_add_bot_1 = State()
    sub_add_bot_2 = State()
    sub_add_channel_1 = State()
    sub_add_channel_2 = State()
    sub_add_show_1 = State()
    sub_add_show_2 = State()
    sub_add_show_3 = State()
    sub_add_show_4 = State()
    sub_delete = State()

    update_text = State()


class WhiteListState(StatesGroup):
    username = State()
    full_name = State()
    position = State()
    competence = State()
    time_zone = State()
    skills = State()
    course = State()
    is_student = State()
