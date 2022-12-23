import asyncio
import datetime
import os

import aiohttp
import pytz
import requests
from dotenv import load_dotenv

load_dotenv()


url = os.environ.get('URL')
bot_token = os.environ.get('TOKEN')

API_link = f'https://api.telegram.org/bot' + bot_token
connect_times = {'prev_time': '', 'curr_time': ''}


async def check_connect(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                return resp.status == 200
        except Exception:
            return False


async def set_time_connect(url):
    while True:
        if await check_connect(url):
            connect_times['curr_time'] = _get_now_formatted()


async def report():
    connect_counter = 0
    connect_state = '🔴 Немає світла'
    current_state = ''
    while True:
        await asyncio.sleep(5)
        if connect_times['prev_time'] != connect_times['curr_time']:
            connect_times['prev_time'] = connect_times['curr_time']
            connect_counter = 0
            connect_state = '🟢 Є світло'
        else:
            if connect_counter < 5:
                connect_counter += 1
            else:
                connect_state = '🔴 Немає світла'
        if current_state != connect_state:
            current_state = connect_state
            msg = f'{current_state}\n{connect_times["curr_time"]}'
            if _is_day():
                requests.get(
                    API_link + f"/sendMessage?chat_id=234043544&text={msg}")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.datetime.now(tz)
    return now


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%H:%M:%S %d-%m-%Y")


def _is_day() -> bool:
    return True
    # return 7 < datetime.datetime.now().hour < 22


async def main():
    tasks = []
    tasks.append(asyncio.ensure_future(set_time_connect(url)))
    tasks.append(asyncio.ensure_future(report()))
    await asyncio.gather(*tasks)


asyncio.run(main())
