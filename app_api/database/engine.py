import time

from app_api.utils import load_config, Settings

from sqlalchemy import select
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app_api.database.models import Base


config: Settings = load_config()


engine = create_async_engine(
    URL(
        'postgresql+asyncpg',
        config.db.user,
        config.db.password,
        config.db.host,
        config.db.port,
        config.db.name,
        query={},
    ), future=True,
    pool_size=20,
)


SessionLocal = async_sessionmaker(engine)


async def get_db() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    session = SessionLocal()

    # a = await session.scalar(
    #     select(Users)
    #     .where(Users.user_id ==  123)
    # )

    # print(a)

    # if a is None:
    #     merge_list = []

    #     new_user = Users(
    #         user_id=123,
    #         username="чума чума"
    #     )

    #     new_student = Students(
    #         user_id=123,
    #         user=new_user
    #     )

    #     new_user_two = Users(
    #         user_id=321,
    #         username="хуй ментор"
    #     )

    #     new_mentor = Mentors(
    #         user_id=321,
    #         user=new_user_two
    #     )

    #     merge_list = [
    #         new_user,
    #         new_user_two,
    #         new_mentor,
    #         new_student
    #     ]

    #     for merge in merge_list:
    #         await session.merge(merge)

    try:
        yield session
    finally:
        # await session.commit()
        await session.close()
