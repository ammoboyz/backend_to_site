import asyncio

from typing import Any, Awaitable, Callable, Dict, Optional
from contextlib import suppress

from aiogram import BaseMiddleware, types, Bot

from sqlalchemy import select
# from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app_bot.templates.texts import user as user_text
from app_bot.database.models import User, Advertising, WhiteList, \
    Student, Mentor, Skill
from app_bot.settings import SEND_EXCEPTIONS


class UserMiddleware(BaseMiddleware):
    """
    Middleware for registering user.
    """

    @staticmethod
    async def plus_ads(
        link: str,
        session: AsyncSession
    ) -> bool:

        ads_link = await session.scalar(
            select(Advertising)
            .where(Advertising.token == link)
        )

        if ads_link is None:
            return False

        ads_link.count += 1
        return True

    async def reg_user(
        self,
        event: types.Update,
        session: AsyncSession,
        event_user: types.User
    ):

        ref_link = ""
        ref_list = []

        if event.message:
            if event.message.text:
                if event.message.text.startswith('/start'):
                    ref_list = event.message.text.split()

        if len(ref_list) == 2:
            ref_link: str = ref_list[1]

        is_ref = await self.plus_ads(ref_link[3:], session)

        white_user = await session.scalar(
            select(WhiteList)
            .where(WhiteList.username == event_user.username)
        )

        new_user = User(
            user_id=event_user.id,
            username=event_user.username,
            full_name=white_user.full_name,
            time_zone=white_user.time_zone,
            where_from=(
                ref_link[3:]
                if ref_link.startswith("ads") and is_ref
                else ""
            ),
        )

        await session.merge(new_user)

        if white_user.is_student:
            new_student = Student(
                user_id=event_user.id,
                user=new_user,
                course=white_user.course
            )
            await session.merge(new_student)
        else:
            new_mentor = Mentor(
                user_id=event_user.id,
                user=new_user,
                position=white_user.position,
                expertise=white_user.competence,
                skills=[
                    Skill(
                        user_id=event_user.id,
                        skill=skill_
                    )
                    for skill_ in white_user.skills.split(",")
                    if white_user.skills.split(",")
                ]
            )
            await session.merge(new_mentor)

        return await self.get_records(session, event_user.id)

    @staticmethod
    async def get_records(
        session: AsyncSession,
        user_id: int
    ):
        user = await session.scalar(
            select(User)
            .where(User.user_id == user_id)
        )

        mentor = await session.scalar(
            select(Mentor)
            .where(Mentor.user_id == user_id)
        )

        student = await session.scalar(
            select(Student)
            .where(Student.user_id == user_id)
        )

        return user, mentor, student

    async def __call__(
        self,
        handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: Dict[str, Any],
    ) -> Any:

        event_user: Optional[types.User] = data.get("event_from_user")
        session: AsyncSession = data['session']
        bot: Bot = data['bot']

        user, mentor, student = await self.get_records(
            session, event_user.id
        )

        if user is None and not event.inline_query:
            user, mentor, student = await self.reg_user(
                event, session, event_user
            )

            with suppress(*SEND_EXCEPTIONS):
                await bot.send_message(
                    chat_id=event_user.id,
                    text=user_text.WELCOME.format(
                        full_name=user.full_name
                    )
                )

            await asyncio.sleep(1)

        # user.last_online = datetime.now()

        if user.dead:
            user.dead = False

        data["user"] = user
        data["mentor"] = mentor
        data["student"] = student

        return await handler(event, data)
