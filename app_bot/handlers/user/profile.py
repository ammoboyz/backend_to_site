import io
import asyncio
from typing import Union

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app_bot.filters.states import UserState
from app_bot.utils import func, Settings, services
from app_bot.templates.texts import buttons, user as user_text
from app_bot.templates.keyboards import user as user_kb
from app_bot.database.models import User, Mentor, Student, Skill


async def profile(
        update: Union[Message, CallbackQuery],
        bot: Bot,
        config: Settings,
        user: User,
        mentor: Mentor,
        student: Student
):

    await bot.send_photo(
        chat_id=update.from_user.id,
        photo=BufferedInputFile(
            await services.get_photo(user.pic_name),
            "image.jpg"
        ),
        caption=func.get_profile_text(student, mentor, user),
        reply_markup=user_kb.inline.profile()
    )


async def change_profile(
        update: Union[Message, CallbackQuery],
        state: FSMContext,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    await state.set_state()

    if isinstance(update, CallbackQuery):
        await update.message.edit_caption(
            caption=user_text.CHANGE_PROFILE.format(
                func.get_profile_text(student, mentor, user)
            ),
            reply_markup=user_kb.inline.change_profile(bool(student))
        )

    elif isinstance(update, Message):
        await update.answer_photo(
            photo=BufferedInputFile(
            await services.get_photo(user.pic_name),
            "image.jpg"
            ),
            caption=user_text.CHANGE_PROFILE.format(
                func.get_profile_text(student, mentor, user)
            ),
            reply_markup=user_kb.inline.change_profile(bool(student))
        )


async def change_full_name(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(UserState.change_full_name)

    await call.message.edit_caption(
        caption=user_text.CHANGE_FULL_NAME,
        reply_markup=user_kb.inline.back_to_profile()
    )


async def input_full_name(
        message: Message,
        state: FSMContext,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    await state.set_state()

    user.full_name = message.text

    await message.reply(
        text=user_text.CHANGE_FULL_NAME_DONE.format(
            message.text
        )
    )

    await asyncio.sleep(1)
    return await change_profile(
        message, state, config, user, student, mentor
    )


async def change_description(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(UserState.change_description)

    await call.message.edit_caption(
        caption=user_text.CHANGE_DESCRIPTION,
        reply_markup=user_kb.inline.back_to_profile()
    )


async def input_description(
        message: Message,
        state: FSMContext,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    await state.set_state()

    user.description = message.text

    await message.reply(
        text=user_text.CHANGE_DESCRIPTION_DONE.format(
            message.text
        )
    )

    await asyncio.sleep(1)
    return await change_profile(
        message, state, config, user, student, mentor
    )


async def change_pic(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(UserState.change_pic)

    await call.message.edit_caption(
        caption=user_text.CHANGE_PIC,
        reply_markup=user_kb.inline.change_pic()
    )


async def input_pic(
        message: Message,
        state: FSMContext,
        bot: Bot,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    if message.document:
        file_name = message.document.file_name
        file_extension = file_name.split('.')[-1].lower()

        if file_extension != "jpg":
            return await message.reply(
                text=user_text.PHOTO_ERROR,
                reply_markup=user_kb.inline.back_to_profile()
            )

    pic_url = await func.download_pic(bot, message, config)

    user.pic_name = pic_url
    await state.set_state()

    await message.reply(
        text=user_text.CHANGE_PIC_DONE
    )

    await asyncio.sleep(1)
    return await change_profile(
        message, state, config, user, student, mentor
    )


async def change_pic_skip(
        call: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    pic_url = await func.download_pic(bot, call, config)

    user.pic_name = pic_url
    await state.set_state()

    await call.message.delete()

    await call.message.answer(
        text=user_text.CHANGE_PIC_DONE
    )

    await asyncio.sleep(1)


    await call.message.answer_photo(
        photo=BufferedInputFile(
            await services.get_photo(user.pic_name),
            "image.jpg"
        ),
        caption=user_text.CHANGE_PROFILE.format(
            func.get_profile_text(student, mentor, user)
        ),
        reply_markup=user_kb.inline.change_profile(bool(student))
    )


async def change_position(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(UserState.change_position)

    await call.message.edit_caption(
        caption=user_text.CHANGE_POSITION,
        reply_markup=user_kb.inline.back_to_profile()
    )


async def input_position(
        message: Message,
        state: FSMContext,
        bot: Bot,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    await state.set_state()

    mentor.position = message.text
    await message.answer(
        text=user_text.CHANGE_POSITION_DONE.format(
            message.text
        )
    )
    await asyncio.sleep(1)
    return await change_profile(
        message, state, config, user, student, mentor
    )


async def change_expertise(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(UserState.change_expertise)

    await call.message.edit_caption(
        caption=user_text.CHANGE_EXPERTISE,
        reply_markup=user_kb.inline.back_to_profile()
    )


async def input_expertise(
        message: Message,
        state: FSMContext,
        config: Settings,
        user: User,
        student: Student,
        mentor: Mentor
):
    await state.set_state()

    mentor.expertise = message.text
    await message.answer(
        text=user_text.CHANGE_EXPERTISE_DONE.format(
            message.text
        )
    )
    await asyncio.sleep(1)
    return await change_profile(
        message, state, config, user, student, mentor
    )


async def change_skill(
        call: CallbackQuery,
        mentor: Mentor
):
    await call.message.edit_caption(
        caption=user_text.CHANGE_SKILLS,
        reply_markup=user_kb.inline.change_skill(mentor.skill_list)
    )


async def input_skill(
        call: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        mentor: Mentor
):
    await state.set_state()
    skill = call.data.split(":")[-1]

    if skill in mentor.skill_list:
        skill_instance = await session.scalar(
            select(Skill)
            .where(Skill.user_id == call.from_user.id)
            .where(Skill.skill == skill)
        )

        await session.execute(
            delete(Skill)
            .where(Skill.user_id == call.from_user.id)
            .where(Skill.skill == skill)
        )

        mentor.skills.remove(skill_instance)
    else:
        mentor.skills.append(
            Skill(
                user_id=call.from_user.id,
                skill=skill
            )
        )

    await call.message.edit_caption(
        caption=user_text.CHANGE_SKILLS,
        reply_markup=user_kb.inline.change_skill(mentor.skill_list)
    )


async def change_time_zone(
        call: CallbackQuery
):
    await call.message.edit_caption(
        caption=user_text.CHANGE_TIME_ZONE,
        reply_markup=user_kb.inline.change_time_zone()
    )


async def input_time_zone(
        call: CallbackQuery,
        user: User
):
    time_zone: int = eval(call.data.split(":")[-1])
    user.time_zone = time_zone

    await call.message.edit_caption(
        caption=user_text.CHANGE_TIME_ZONE_DONE.format(
            time_zone
        ),
        reply_markup=user_kb.inline.back_to_profile()
    )


def register(router: Router):
    router.message.register(
        profile,
        or_f(
            F.text == buttons.PROFILE,
            Command("profile")
        )
    )
    router.message.register(
        change_profile,
        or_f(
            F.text == buttons.CHANGE_PROFILE,
            Command("edit")
        )
    )
    router.callback_query.register(
        change_profile,
        F.data == "change_profile"
    )

    router.callback_query.register(
        change_full_name,
        F.data == "change_profile:full_name"
    )
    router.message.register(
        input_full_name,
        F.text,
        F.text.len() < 500,
        StateFilter(UserState.change_full_name)
    )

    router.callback_query.register(
        change_description,
        F.data == "change_profile:description"
    )
    router.message.register(
        input_description,
        F.text,
        F.text.len() < 500,
        StateFilter(UserState.change_description)
    )

    router.callback_query.register(
        change_pic,
        F.data == "change_profile:pic"
    )
    router.message.register(
        input_pic,
        StateFilter(UserState.change_pic),
        or_f(
            F.photo,
            F.document
        )
    )
    router.callback_query.register(
        change_pic_skip,
        F.data == "change_pic:skip"
    )

    router.callback_query.register(
        change_skill,
        F.data == "change_profile:skill"
    )
    router.callback_query.register(
        input_skill,
        F.data.startswith("input_skill:")
    )

    router.callback_query.register(
        change_expertise,
        F.data == "change_profile:expertise"
    )
    router.message.register(
        input_expertise,
        F.text,
        F.text.len() < 500,
        StateFilter(UserState.change_expertise)
    )

    router.callback_query.register(
        change_position,
        F.data == "change_profile:position"
    )
    router.message.register(
        input_position,
        F.text,
        F.text.len() < 500,
        StateFilter(UserState.change_position)
    )

    router.callback_query.register(
        change_time_zone,
        F.data == "change_profile:time_zone"
    )
    router.callback_query.register(
        input_time_zone,
        F.data.startswith("input_time_zone:")
    )
