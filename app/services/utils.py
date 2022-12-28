import datetime

import pytz


TZ = pytz.timezone("Europe/Kiev")

def _get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ)
    return now


def get_now_formatted() -> str:
    return _get_now_datetime().strftime("%H:%M:%S %d-%m-%Y")


def is_day() -> bool:
    return 7 < datetime.datetime.now(TZ).hour < 24
