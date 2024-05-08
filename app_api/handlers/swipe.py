from contextlib import suppress

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram import Bot
from aiogram.types import BufferedInputFile

from app_bot.utils import services
from app_bot.templates.keyboards import user as user_kb
from app_bot.templates.texts import user as user_text
from app_bot.settings import SEND_EXCEPTIONS

from app_api.database import get_db
from app_api.utils import func, Settings
from app_api.database.models import Mentor, Like, Dislike, \
    Favourite, Student


async def get_swipe(
        request: Request,
        skills: str = None,
        cons_type: str = None,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    is_student = await func.check_user(
        user_id=user_id,
        model=Student,
        session=session
    )

    if not is_student:
        return JSONResponse(
            status_code=400,
            content={"message": "This user_id is not student!"}
        )

    # completed_likes = union(
    #     select(Like.second_id).where(
    #         Like.first_id == user_id
    #     ),
    #     select(Dislike.second_id).where(
    #         Dislike.first_id == user_id
    #     )
    # )

    match_select = (
        select(Mentor)
        # .where(~ Mentor.user_id.in_(completed_likes))
    )

    # if skills:
    #     match_select = match_select.where(
    #         Mentor.skills.
    #         # Mentor.skills.in_(skills.split(","))
    #     )

    if cons_type:
        match_select = match_select.where(
            Mentor.cons_type == cons_type
        )

    mentors_sequence = (await session.scalars(
        match_select
    )).all()

    mentors_list = []

    for mentor in mentors_sequence:
        mentors_list.append({
            "user_id": mentor.user_id,
            "full_name": mentor.user.full_name,
            # "pic_url": mentor.user.get_pic_url(request.base_url),
            "skills": mentor.skill_list,
            "description": mentor.user.description,
            "cons_type": mentor.cons_type
        })

    await session.commit()
    return JSONResponse(status_code=200, content=mentors_list)


async def like(
        request: Request,
        message: str,
        second_id: int,
        send_like: bool,
        session: AsyncSession = Depends(get_db)
):
    first_id: int = request.state.user_id
    bot: Bot = request.state.bot
    config: Settings = request.state.config

    student = await session.scalar(
        select(Student)
        .where(Student.user_id == first_id)
    )

    if not student:
        return JSONResponse(
            status_code=400,
            content={"message": "user_id is not student!"}
        )

    is_already = await session.scalar(
        select(Like)
        .where(Like.first_id == first_id)
        .where(Like.second_id == second_id)
        .where(Like.is_approved == None)
    )

    if is_already:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"User already "
                           f"added like to {second_id}"
            }
        )

    new_favourite = Favourite(
        first_id=first_id,
        second_id=second_id
    )

    await session.merge(new_favourite)

    if send_like:
        new_like = Like(
            first_id=first_id,
            second_id=second_id,
            message=message
        )

        with suppress(*SEND_EXCEPTIONS):
            await bot.send_photo(
                chat_id=second_id,
                photo=BufferedInputFile(
                    await services.get_photo(student.user.pic_name),
                    'image.jpg'
                ),
                caption=user_text.lIKE_ADDED.format(
                    full_name=student.user.full_name,
                    description=student.user.description,
                    course=student.course,
                    message=message or "отсутствует"
                ),
                reply_markup=user_kb.inline.webapp(config)
            )

        await session.merge(new_like)
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Like added!"}
    )


async def dislike(
        request: Request,
        second_id: int = None,
        send_like: bool = None,
        message: str = "",
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    is_already = await session.scalar(
        select(Dislike)
        .where(Dislike.first_id == user_id)
        .where(Dislike.second_id == second_id)
    )

    if is_already:
        return JSONResponse(
            status_code=200,
            content={"message": "Already disliked!"}
        )

    mentor = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == second_id)
    )

    if mentor is None:
        return JSONResponse(
            status_code=400,
            content={"message": "second_id is null from database!"}
        )

    new_dislike = Dislike(
        first_id=user_id,
        second_id=second_id
    )

    await session.merge(new_dislike)
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Dislike added!"}
    )


def register(app: FastAPI):
    app.add_api_route("/swipe/get", get_swipe, methods=["GET"])
    app.add_api_route("/swipe/like", like, methods=["POST"])
    app.add_api_route("/swipe/dislike", dislike, methods=["POST"])
