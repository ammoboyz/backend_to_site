from datetime import datetime

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app_api.database import get_db
from app_api.utils import func
from app_api.database.models import Meeting, Date, Mentor


async def date_add(
        request: Request,
        week_day: int,
        hours: int,
        minutes: int,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    profile = await session.scalar(
        select(Mentor)
        .where(Mentor.user_id == user_id)
    )

    already_data = await session.scalar(
        select(Date)
        .where(Date.user_id == user_id)
        .where(Date.week_day == week_day)
        .where(Date.hours == hours)
        .where(Date.minutes == minutes)
    )

    if already_data:
        return JSONResponse(
            status_code=400,
            content={"message": "Date already added!"}
        )

    new_date = Date(
        user_id=user_id,
        week_day=week_day,
        hours=hours,
        minutes=minutes
    )

    profile.dates.append(new_date)
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Date added!"}
    )


async def date_get(
        request: Request,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    date_list = (await session.scalars(
        select(Date)
        .where(Date.user_id == user_id)
    )).all()

    date_busy_list = (await session.scalars(
        select(Meeting.date_id)
        .where(Meeting.second_id == user_id)
        .where(Meeting.meeting_date >= datetime.now())
    )).all()

    result = {
        "user_id": user_id,
        "date_list": [
            {
                "id": date.id,
                "date": func.next_weekday(
                    date.week_day,
                    date.hours,
                    date.minutes
                ).isoformat(),
                "is_busy": date.id in date_busy_list
            }
            for date in date_list
        ]
    }

    await session.commit()
    return JSONResponse(
        status_code=200,
        content=result
    )


async def date_delete(
        request: Request,
        date_id: int,
        session: AsyncSession = Depends(get_db)
):
    user_id: int = request.state.user_id

    await session.execute(
        delete(Date)
        .where(Date.id == date_id)
        .where(Date.user_id == user_id)
    )

    await session.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Date removed!"}
    )


def register(app: FastAPI):
    app.add_api_route("/date/add", date_add, methods=["POST"])
    app.add_api_route("/date/get", date_get, methods=["GET"])
    app.add_api_route("/date/delete", date_delete, methods=["POST"])