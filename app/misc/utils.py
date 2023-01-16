import datetime

import pytz


TZ = pytz.timezone("Europe/Kiev")

async def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ)
    return now


async def get_now_formatted() -> str:
    return await get_now_datetime().strftime("%H:%M:%S %d-%m-%Y")


async def is_day() -> bool:
    return 7 < datetime.datetime.now(TZ).hour < 24
