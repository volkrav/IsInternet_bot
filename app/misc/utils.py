import datetime

import pytz

TZ = pytz.timezone("Europe/Kiev")


async def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ).replace(tzinfo=None)
    return now


async def get_now_formatted() -> str:
    now_datetime = await get_now_datetime()
    return now_datetime.strftime("%H:%M %d.%m.%Y")


async def is_day() -> bool:
    return 6 < datetime.datetime.now(TZ).hour < 23
