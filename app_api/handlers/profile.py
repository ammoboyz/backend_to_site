from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from contextlib import suppress
from aiogram import Dispatcher, Bot
from aiogram.types import BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_bot.utils import services
from app_bot.filters.states import UserState
from app_bot.templates.texts import user as user_text
from app_bot.templates.keyboards import user as user_kb
from app_bot.settings import SEND_EXCEPTIONS

from app_api.database import get_db
from app_api.utils import func
from app_api.database.models import Student, Mentor, User


def user_exception():
    return JSONResponse(
        status_code=400,
        content={
            "message": "user_id is None from database."
        }
    )


async def get_profile(
        request: Request,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    is_student = await func.check_user(
        user_id=user_id,
        model=Student,
        session=session
    )

    if is_student:
        student = await session.scalar(
            select(Student)
            .where(Student.user_id == user_id)
        )

        result = {
            "user_id": user_id,
            "is_student": True,
            "full_name": student.user.full_name,
            # "pic_url": student.user.get_pic_url(request.base_url),
            "description": student.user.description,
            "course": student.course,
        }

    else:
        mentor = await session.scalar(
            select(Mentor)
            .where(Mentor.user_id == user_id)
        )

        if mentor is None:
            return user_exception()

        result = {
            "user_id": user_id,
            "is_student": False,
            "full_name": mentor.user.full_name,
            # "pic_url": mentor.user.get_pic_url(request.base_url),
            "description": mentor.user.description,

            "rating": (
                sum(
                    [feedback.score for feedback in mentor.feedbacks]
                ) / len(mentor.feedbacks)
                if mentor.feedbacks else None
            ),
            "position": mentor.position,
            "expertise": mentor.expertise,
            "skills": mentor.skill_list,
            "feedbacks": (
                [
                    {
                        "score": feedback.score,
                        "description": feedback.description
                    }
                    for feedback in mentor.feedbacks
                ]
                if mentor.feedbacks else []
            ),
            "time_zone": mentor.user.time_zone,
            "contact_in_week": mentor.limit_in_week
        }

    return JSONResponse(
        status_code=200,
        content=result
    )


async def change_course(
        request: Request
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    dp: Dispatcher = request.state.dp

    state = await func.state_with(
        user_id=user_id,
        bot=bot,
        dp=dp
    )

    await state.set_state(UserState.change_course)

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_message(
            chat_id=user_id,
            text=user_text.CHANGE_COURSE,
            reply_markup=user_kb.inline.change_course()
        )

    return JSONResponse(
        status_code=200,
        content={"message": "course changed"}
    )


async def change_pic(
        request: Request,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    dp: Dispatcher = request.state.dp

    user = await session.scalar(
        select(User)
        .where(User.user_id == user_id)
    )

    state = await func.state_with(
        user_id=user_id,
        bot=bot,
        dp=dp
    )

    await state.set_state(UserState.change_pic)

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_photo(
            chat_id=user_id,
            photo=BufferedInputFile(
                await services.get_photo(user.pic_name),
                "image.jpg"
            ),
            caption=user_text.CHANGE_PIC,
            reply_markup=user_kb.inline.change_pic()
        )

    return JSONResponse(
        status_code=200,
        content={"message": "pic changed"}
    )


async def change_description(
        request: Request
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    dp: Dispatcher = request.state.dp

    state = await func.state_with(
        user_id=user_id,
        bot=bot,
        dp=dp
    )

    await state.set_state(
        UserState.change_description
    )

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_message(
            chat_id=user_id,
            text=user_text.CHANGE_DESCRIPTION,
            reply_markup=user_kb.inline.back_to_profile()
        )

    return JSONResponse(
        status_code=200,
        content={"message": "description changed"}
    )


def register(app: FastAPI):
    app.add_api_route("/profile/get", get_profile, methods=["GET"])
    app.add_api_route("/profile/change/course", change_course, methods=["POST"])
    app.add_api_route("/profile/change/pic", change_pic, methods=["POST"])
    app.add_api_route("/profile/change/description", change_description, methods=["POST"])
