import datetime
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER

from app_bot.database.models import User


async def user_blocked_bot(event: ChatMemberUpdated, user: User):
    user.dead_date = datetime.date.today()
    user.dead = True


async def user_unblocked_bot(event: ChatMemberUpdated, user: User):
    user.dead_date = None
    user.dead = False


def register(router: Router):
    router.my_chat_member.register(
        user_blocked_bot,
        ChatMemberUpdatedFilter(
            member_status_changed=KICKED
        ),
        F.chat.type == "private"
    )
    router.my_chat_member.register(
        user_unblocked_bot,
        ChatMemberUpdatedFilter(
            member_status_changed=MEMBER
        ),
        F.chat.type == "private"
    )
