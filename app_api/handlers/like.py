from contextlib import suppress

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from aiogram import Bot

from app_bot.templates.keyboards import user as user_kb
from app_bot.templates.texts import user as user_text
from app_bot.settings import SEND_EXCEPTIONS

from app_api.database import get_db
from app_api.utils import Settings, func
from app_api.database.models import Like, Favourite, \
    Student, Mentor


async def like_get(
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
        condition = Like.first_id == user_id
        user_full_name = "like.mentor.user.full_name"
    else:
        condition = Like.second_id == user_id
        user_full_name = "like.student.user.full_name"

    like_list = (await session.scalars(
        select(Like)
        .where(condition)
    )).all()

    result = {
        "user_id": user_id,
        "is_student": bool(is_student),
        "like_list": [
            {
                "id": like.id,
                "user_id": (
                    like.first_id
                    if like.first_id != user_id
                    else like.second_id
                ),
                # "pic_url": eval(user_pic_url),
                "full_name": eval(user_full_name),
                "create_date": like.create_date.isoformat(),
                "is_approved": like.is_approved,
                "message": like.message,
                "answer": like.answer
            }
            for like in like_list
        ]
    }

    return JSONResponse(
        status_code=200,
        content=result
    )


async def like_answer(
        request: Request,
        id: int,
        is_approved: bool,
        answer: str = "",
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id
    bot: Bot = request.state.bot
    config: Settings = request.state.config

    like = await session.scalar(
        select(Like)
        .where(Like.id == id)
    )

    if like is None:
        return JSONResponse(
            status_code=400,
            content={"message": "Like id is null from database!"}
        )

    if like.is_approved is not None:
        return JSONResponse(
            status_code=400,
            content={"message": "like already approved!"}
        )

    is_mentor = await func.check_user(
        user_id=user_id,
        model=Mentor,
        session=session
    )

    if not is_mentor:
        return JSONResponse(
            status_code=400,
            content={"message": "first_id is not mentor!"}
        )

    if like.is_approved == True or like.is_approved == False:
        return JSONResponse(
            status_code=400,
            content={"message": "Like already answered!"}
        )

    if is_approved:
        like.is_approved = True

        with suppress(*SEND_EXCEPTIONS):
            await bot.send_message(
                chat_id=like.first_id,
                text=user_text.LIKE_APPROVED.format(
                    username=like.mentor.user.username,
                    full_name=like.mentor.user.full_name
                ),
                reply_markup=user_kb.inline.webapp(config)
            )
    else:
        with suppress(*SEND_EXCEPTIONS):
            await bot.send_message(
                chat_id=like.first_id,
                text=user_text.LIKE_NOT_APPROVED.format(
                    username=like.mentor.user.username,
                    full_name=like.mentor.user.full_name
                ),
                reply_markup=user_kb.inline.webapp(config)
            )

        like.is_approved = False
        like.answer = answer

    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "like answer done."}
    )


async def favourite_get(
        request: Request,
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
            content={"message": "This user is not student!"}
        )

    profile = await session.scalar(
        select(Student)
        .where(Student.user_id == user_id)
    )

    result = {
        "user_id": user_id,
        "favourite_list": [
            {
                "id": favourite.id,
                "second_id": favourite.second_id,
                # "pic_url": favourite.mentor.user.get_pic_url(request.base_url),
                "full_name": favourite.mentor.user.full_name,
                "create_date": favourite.create_date.isoformat()
            }
        for favourite in profile.favourites
        ]
        if profile.favourites else []
    }

    return JSONResponse(
        status_code=200,
        content=result
    )


async def favourite_delete(
        request: Request,
        id: int,
        session: AsyncSession = Depends(get_db)
):
    await session.execute(
        delete(Favourite)
        .where(Favourite.id == id)
    )

    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "favourite deleted"}
    )


def register(app: FastAPI):
    app.add_api_route("/like/get", like_get, methods=["GET"])
    app.add_api_route("/like/answer", like_answer, methods=["POST"])
    app.add_api_route("/like/favourite/get", favourite_get, methods=["GET"])
    app.add_api_route("/like/favourite/delete", favourite_delete, methods=["POST"])
