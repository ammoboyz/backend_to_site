from datetime import datetime
from contextlib import suppress

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram import Bot

from app_bot.templates.keyboards import user as user_kb
from app_bot.templates.texts import user as user_text
from app_bot.settings import SEND_EXCEPTIONS

from app_api.database import get_db
from app_api.utils import Settings, func
from app_api.database.models import Meeting, Date, Mentor, \
    Feedback, Student, User


async def meeting_add(
        request: Request,
        second_id: int,
        date_id: int,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    config: Settings = request.state.config

    student = await session.scalar(
        select(Student)
        .where(Student.user_id == user_id)
    )

    meeting_busy = await session.scalar(
        select(Meeting)
        .where(Meeting.date_id == date_id)
        .where(Meeting.meeting_date >= datetime.now())
    )

    if meeting_busy:
        return JSONResponse(
            status_code=400,
            content={"message": "Is date already busy!"}
        )

    date = await session.scalar(
        select(Date)
        .where(Date.id == date_id)
    )

    if not date:
        return JSONResponse(
            status_code=400,
            content={"message": "Date not found."}
        )

    new_meeting = Meeting(
        date_id=date_id,
        first_id=user_id,
        second_id=second_id,
        meeting_date=func.next_weekday(
            date.week_day,
            date.hours,
            date.minutes
        ),
    )

    await session.merge(new_meeting)

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_message(
            chat_id=second_id,
            text=user_text.MEETING_ADD.format(
                username=student.user.username,
                full_name=student.user.full_name
            ),
            disable_web_page_preview=True,
            reply_markup=user_kb.inline.webapp(config)
        )

    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Meeting added!"}
    )


async def feedback_add(
    request: Request,
    second_id: int,
    score: int,
    message: str,
    session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    config: Settings = request.state.config

    already_feedback = await session.scalar(
        select(Feedback)
        .where(Feedback.first_id == user_id)
        .where(Feedback.second_id == second_id)
    )

    if already_feedback:
        return JSONResponse(
            status_code=400,
            content={"message": "feedback already sended!"}
        )

    mentor = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == second_id)
    )

    if not mentor:
        return JSONResponse(
            status_code=400,
            content={"message": "second_id is null from database!"}
        )

    student = await session.scalar(
        select(Student)
        .where(Student.user_id == user_id)
    )

    new_feedback = Feedback(
        first_id=user_id,
        second_id=second_id,
        description=message,
        score=score
    )

    mentor.feedbacks.append(new_feedback)

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_message(
            chat_id=second_id,
            text=user_text.FEEDBACK_ADD.format(
                username=student.user.username,
                full_name=student.user.full_name,
                score=score,
                description=(
                    message
                    or "отсутствует"
                )
            ),
            disable_web_page_preview=True,
            reply_markup=user_kb.inline.webapp(config)
        )

    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Feedback added!"}
    )


async def meeting_get(
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
        meeting_list = (await session.scalars(
            select(Meeting)
            .where(Meeting.first_id == user_id)
        )).all()

        result = {
            "user_id": user_id,
            "meetings": [
                {
                    "user_id": meeting.second_id,
                    "full_name": meeting.mentor.user.full_name,
                    # "pic_url": meeting.mentor.user.get_pic_url(request.base_url),
                    "date": meeting.meeting_date.isoformat(),
                    "is_old": (
                        meeting.meeting_date < datetime.now()
                    )
                }
                for meeting in meeting_list
            ]
        }

    else:
        meeting_list = (await session.scalars(
            select(Meeting)
            .where(Meeting.second_id == user_id)
        ))

        result = {
            "user_id": user_id,
            "meetings": [
                {
                    "user_id": meeting.first_id,
                    "full_name": meeting.student.user.full_name,
                    # "pic_url": meeting.student.user.get_pic_url(request.base_url),
                    "date": meeting.meeting_date.isoformat(),
                    "is_old": (
                        meeting.meeting_date < datetime.now()
                    )
                }
                for meeting in meeting_list
            ]
        }

    return JSONResponse(
        status_code=200,
        content=result
    )


async def meeting_contact(
        request: Request,
        second_id: int,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot

    second_user = await session.scalar(
        select(User)
        .where(User.user_id == second_id)
    )

    if not second_user:
        return JSONResponse(
            status_code=400,
            content={"message": "second_user is null from database!"}
        )

    with suppress(*SEND_EXCEPTIONS):
        await bot.send_message(
            chat_id=user_id,
            text=user_text.MEETING_CONTACT,
            reply_markup=user_kb.inline.meeting_contact(
                second_user.username
            )
        )

    return JSONResponse(
        status_code=200,
        content={"message": "Contact done!"}
    )


def register(app: FastAPI):
    app.add_api_route("/meeting/add", meeting_add, methods=["POST"])
    app.add_api_route("/meeting/get", meeting_get, methods=["GET"])
    app.add_api_route("/meeting/contact", meeting_contact, methods=["POST"])

    app.add_api_route("/meeting/feedback/add", feedback_add, methods=["POST"])
