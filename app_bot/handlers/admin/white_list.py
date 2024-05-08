from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app_general.models import WhiteList
from app_bot.filters.states import WhiteListState
from app_bot.templates.keyboards import admin as admin_kb


async def plus_white_list(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(WhiteListState.username)

    await call.message.edit_text(
        text="➕ Введите юзернейм нового пользователя",
        reply_markup=admin_kb.inline.admin_back()
    )


async def input_username(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        username=message.text.replace("@", "")
    )

    await state.set_state(WhiteListState.full_name)

    await message.answer(
        text="➕ Введите полное имя (Имя Фамилия) пользователя",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_full_name(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        full_name=message.text
    )

    await state.set_state(WhiteListState.position)

    await message.answer(
        text="➕ Напишите должность если это ментор. Если должности нету, пишем -.",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_position(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        position=(
            ""
            if message.text == "-"
            else message.text
        )
    )

    await state.set_state(
        WhiteListState.competence
    )

    await message.answer(
        text="➕ Напишите экспертизу если это ментор, иначе напишите -.",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_competence(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        competence=(
            ""
            if message.text == "-"
            else message.text
        )
    )

    await state.set_state(WhiteListState.time_zone)

    await message.answer(
        text="➕ Введите от -12 до 12 в формате GMT часовой пояс пользователя.",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_time_zone(
        message: Message,
        state: FSMContext
):
    if not type(eval(message.text)) == int:
        return await message.answer(
            text="➕ Число введено неверно. Введите от -12 до 12 в формате GMT часовой пояс пользователя.",
            reply_markup=admin_kb.inline.go_back()
        )

    await state.update_data(
        time_zone=int(message.text)
    )

    await state.set_state(WhiteListState.skills)

    await message.answer(
        text="➕ Перечислите через запятую сферы экспертиз если это ментор. В противном случае '-'."
             "\n\n<code>Python,Информационные технологи</code>",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_skills(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        skills=message.text
    )

    await state.set_state(WhiteListState.course)

    await message.answer(
        text="➕ Введите курс если это студент от 1 до 2. В противном случае введите 0.",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_course(
        message: Message,
        state: FSMContext
):
    await state.update_data(
        course=int(message.text)
    )

    await state.set_state(WhiteListState.is_student)

    await message.answer(
        text="➕ Введите 1 если добавляем студента, если ментора то 0.",
        reply_markup=admin_kb.inline.go_back()
    )


async def input_student(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    if not message.text.isdigit():
        return await message.answer(
            text="➕ Нужно ввести число!"
        )

    fsm_data = await state.update_data(
        is_student=bool(int(message.text))
    )

    new_white_list = WhiteList(
        username=fsm_data.get('username'),
        full_name=fsm_data.get('full_name'),
        is_student=fsm_data.get('is_student'),
        competence=fsm_data.get('competence'),
        time_zone=fsm_data.get('time_zone'),
        skills=fsm_data.get('skills'),
        course=fsm_data.get('course')
    )

    await session.merge(new_white_list)

    await message.answer(
        text=f"➕ Пользователь @{fsm_data.get('username')} успешно добавлен в белый список!",
        reply_markup=admin_kb.inline.go_back()
    )


def register(router: Router):
    router.callback_query.register(plus_white_list, F.data == "white_list:add")
    router.message.register(input_username, F.text, WhiteListState.username)
    router.message.register(input_full_name, F.text, WhiteListState.full_name)
    router.message.register(input_position, F.text, WhiteListState.position)
    router.message.register(input_competence, F.text, WhiteListState.competence)
    router.message.register(input_time_zone, F.text, WhiteListState.time_zone)
    router.message.register(input_skills, F.text, WhiteListState.skills)
    router.message.register(input_course, F.text, WhiteListState.course)
    router.message.register(input_student, F.text, WhiteListState.is_student)
