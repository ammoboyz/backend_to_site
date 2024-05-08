import datetime
import io, os
import matplotlib.pyplot as plt

from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_bot.database.models import User, Advertising, Student, Mentor, Meeting


class StatisticsPlotter:
    """A class to generate and plot statistics based on registration, blockage.

    Args:
        interval (int): The number of days for the interval.
        date_reg (list): List of dates for registrations.
        date_dead (list): List of dates for blockages.
        label_reg (str, optional): Label for registration data. Defaults to "Registration".
        label_dead (str, optional): Label for blockage data. Defaults to "Blockage".

    Methods:
        generate_data: Generates data based on the provided intervals and dates.
        plot_statistics: Plots statistics for the given data and returns an image buffer in BytesIO format.
    """

    def __init__(
            self,
            interval: int,
            session: AsyncSession,
            show_id: int = None,
            ads_token: str = None,
            label_reg: str = "Переходов",
            label_dead: str = "Блокировка"
    ) -> None:

        self.today = datetime.date.today()
        self.show_id = show_id
        self.interval = interval
        self.session = session
        self.ads_token = ads_token

        self.label_reg = label_reg
        self.label_dead = label_dead

    @staticmethod
    def formatted_integer(integer: int) -> str:
        if integer < 1000:
            return str(integer)

        prefix = ""

        while integer >= 1000:
            integer //= 1000
            prefix = prefix + "к"

        result = f"{integer}{prefix}"
        return result


    def generate_data(self):
        data = []

        for i in range(self.interval - 1, -1, -1):
            count_reg = self.date_reg.count(self.today - datetime.timedelta(days=i))
            count_dead = self.date_dead.count(self.today - datetime.timedelta(days=i))

            data.append((count_reg, count_dead))

        end_date = self.today
        date_list = [end_date - datetime.timedelta(days=i) for i in range(self.interval - 1, -1, -1)]
        days = [date.strftime("%d.%m.%Y") for date in date_list]

        return data, days


    async def _request_session(self) -> None:
        users_match = select(User)

        if self.ads_token is not None:
            users_match = users_match.where(
                User.where_from == self.ads_token
            )

        users_list = (await self.session.scalars(
            users_match
        )).all()

        self.date_dead = [date_element.dead_date for date_element in users_list]
        self.date_reg = [date_element.reg_date for date_element in users_list]


    async def plot_statistics(self) -> io.BytesIO:
        await self._request_session()
        data, days = self.generate_data()

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.set_title(f"Статистика за последние {self.interval} дней")
        ax.set_xlabel("Дни")
        ax.set_ylabel("Количество")

        registration = [day[0] for day in data]
        deaths = [day[1] for day in data]

        bar_width = 0.4
        step = 0.2

        ax.bar([i - step for i in range(len(days))], registration, width=bar_width, label=self.label_reg, color="blue")
        ax.bar([i + step for i in range(len(days))], deaths, width=bar_width, label=self.label_dead, color="red")

        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days)
        plt.xticks(rotation=45, fontsize=8)
        ax.legend()

        reqs_empty = registration.count(0) == self.interval
        deads_empty = deaths.count(0) == self.interval

        if not (reqs_empty and deads_empty):
            for i, v in enumerate(registration):
                ax.text(i - step, v + 0.005, self.formatted_integer(v), ha='center', va='bottom')
            for i, v in enumerate(deaths):
                ax.text(i + step, v + 0.005, self.formatted_integer(v), ha='center', va='bottom')

        buff = io.BytesIO()
        plt.savefig(buff, format="png")

        plt.close()

        return buff


class StatisticString:
    def __init__(
        self,
        session: AsyncSession,
        ads: Advertising = None,
        ads_token: str = None,
        bot_username: str = None
    ):

        self.ads = ads
        self.ads_token = ads_token
        self.session = session
        self.bot_username = bot_username


    def _cycle(self) -> None:
        today = datetime.date.today()

        self.count_dead = 0

        self.count_ads_today = 0
        self.count_ads_week = 0
        self.count_ads_month = 0

        self.count_samorost_today = 0
        self.count_samorost_week = 0
        self.count_samorost_month = 0

        self.count_dead_today = 0
        self.count_dead_week = 0
        self.count_dead_month = 0

        for user in self.users_list:
            if today == user.reg_date:
                if user.where_from:
                    self.count_ads_today += 1
                else:
                    self.count_samorost_today += 1

            if (today - user.reg_date).days <= 7:
                if user.where_from:
                    self.count_ads_week += 1
                else:
                    self.count_samorost_week += 1

            if (today - user.reg_date).days <= 30:
                if user.where_from:
                    self.count_ads_month += 1
                else:
                    self.count_samorost_month += 1

            if user.dead:
                self.count_dead += 1

                if today == user.dead_date:
                    self.count_dead_today += 1

                if (today - user.dead_date).days <= 7:
                    self.count_dead_week += 1

                if (today - user.dead_date).days <= 30:
                    self.count_dead_month += 1

    async def _request_session(self) -> None:
        users_match = select(User)

        if self.ads_token is not None:
            self.ads = await self.session.scalar(
                select(Advertising)
                .where(Advertising.token == self.ads_token)
            )

            users_match = users_match.where(
                User.where_from == self.ads_token
            )

        self.users_list = (await self.session.scalars(
            users_match
        )).all()

        self.meeting_list = (await self.session.scalars(
            select(Meeting)
        )).all()

        self.mentor_list = (await self.session.scalars(
            select(Mentor)
        )).all()

        self.student_list = (await self.session.scalars(
            select(Student)
        )).all()

    async def ads_statistics(self) -> str:
        await self._request_session()
        self._cycle()

        return f'''
<b>📊 Статистика ссылки {self.ads.name}:</b>

<b>🗓 Cоздан:</b> <code>{self.ads.date.strftime('%d.%m.%Y %H:%M:%S')}</code>


<b>👥 Переходов по ссылке:</b> <code>{len(self.users_list)}</code>

<b>👨‍🦱 Живые пользователи:</b> <code>{len(self.users_list) - self.count_dead}</code>
<b>💀 Мёртвых пользователей:</b> <code>{self.count_dead}</code>

<b>💸 Реклама за сегодня:</b> <code>{self.count_ads_today}</code>
<b>💸 Реклама за неделю:</b> <code>{self.count_ads_week}</code>
<b>💸 Реклама за месяц:</b> <code>{self.count_ads_month}</code>

<b>💀 Умерло за сегодня:</b> <code>{self.count_dead_today}</code>
<b>💀 Умерло за неделю:</b> <code>{self.count_dead_week}</code>
<b>💀 Умерло за месяц:</b> <code>{self.count_dead_month}</code>

<b>🔗 Ссылка:</b> <code>https://t.me/{self.bot_username}?start=ads{self.ads.token}</code>
'''


    async def all_statistics(self) -> str:
        await self._request_session()
        self._cycle()

        return f'''
<b>📊 Статистика:</b>

<b>👥 Всего пользователей:</b> <code>{len(self.users_list)}</code>

<b>👨‍🦱 Живые пользователи:</b> <code>{len(self.users_list) - self.count_dead}</code>
<b>💀 Мёртвых пользователей:</b> <code>{self.count_dead}</code>

<b>👨‍🏫 Менторов:</b> <code>{len(self.mentor_list)}</code>
<b>👨‍🎓 Студентов:</b> <code>{len(self.student_list)}</code>
<b>🤝 Количество встреч:</b> <code>{len(self.meeting_list)}</code>

<b>👨‍👩‍👧‍👦 Всего за сегодня:</b> <code>{self.count_ads_today + self.count_samorost_today}</code>
<b>👨‍👩‍👧‍👦 Всего за неделю:</b> <code>{self.count_ads_week + self.count_samorost_week}</code>
<b>👨‍👩‍👧‍👦 Всего за месяц:</b> <code>{self.count_ads_month + self.count_samorost_month}</code>

<b>📈 Cаморост за сегодня:</b> <code>{self.count_samorost_today}</code>
<b>📈 Cаморост за неделю:</b> <code>{self.count_samorost_week}</code>
<b>📈 Cаморост за месяц:</b> <code>{self.count_samorost_month}</code>

<b>💸 Реклама за сегодня:</b> <code>{self.count_ads_today}</code>
<b>💸 Реклама за неделю:</b> <code>{self.count_ads_week}</code>
<b>💸 Реклама за месяц:</b> <code>{self.count_ads_month}</code>

<b>💀 Умерло за сегодня:</b> <code>{self.count_dead_today}</code>
<b>💀 Умерло за неделю:</b> <code>{self.count_dead_week}</code>
<b>💀 Умерло за месяц:</b> <code>{self.count_dead_month}</code>
'''


async def report(text: str, list_id: list, bot: Bot) -> None:
    for user_id in list_id:
        await bot.send_message(
            chat_id=user_id,
            text=text
        )
