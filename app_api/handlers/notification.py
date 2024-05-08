from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app_api.database import get_db
from app_api.database.models import Student, Like


async def get_notification(
        request: Request,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    student = await session.scalar(
        select(Student)
        .where(Student.user_id == user_id)
    )

    if not student:
        return JSONResponse(
            status_code=400,
            content={"message": "user is not student!"}
        )

    like_list = (await session.scalars(
        select(Like)
        .where(Like.first_id == user_id)
    )).all()

    notification_list = []
    for like in like_list:
        notification_list.append({
            "type": "like",
            "user_id": like.second_id,
            "is_approved": like.is_approved,
            "message": like.answer,
            # "pic_url": like.mentor.user.get_pic_url(request.base_url)
        })

    result = {
        "user_id": user_id,
        "notification_list": notification_list
    }

    return JSONResponse(
        status_code=200,
        content=result
    )


def register(app: FastAPI):
    app.add_api_route("/notification/get", get_notification, methods=["GET"])
