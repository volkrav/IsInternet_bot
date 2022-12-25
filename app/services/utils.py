import datetime

import pytz


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.datetime.now(tz)
    return now


def get_now_formatted() -> str:
    return _get_now_datetime().strftime("%H:%M:%S %d-%m-%Y")


def is_day() -> bool:
    return 7 < datetime.datetime.now().hour < 24
