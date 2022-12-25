import asyncio
import datetime
import os

import aiohttp
import pytz
from dotenv import load_dotenv

load_dotenv()


url = os.environ.get('URL')
bot_token = os.environ.get('TOKEN')
chat_id = os.environ.get('CHAT_ID')
port = os.environ.get('PORT')
port = os.environ.get('PORT')

API_link = f'https://api.telegram.org/bot' + bot_token
connect_times = {'prev_time': '', 'curr_time': ''}

PING = True


async def sending_ping_request(_, ip) -> bool:
    reply = await asyncio.create_subprocess_shell(
        f"ping -c 1 -n {ip}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await reply.communicate()

    return reply.returncode == 0


async def sending_web_request(session, url) -> bool:
    try:
        async with session.get(url) as resp:
            return resp.status == 200
    except Exception:
        return False


async def set_time_connect(session, url) -> None:
    if PING:
        check_connect = sending_ping_request
    else:
        check_connect = sending_web_request
        url = 'http://' + url + ':' + port + '/'
    while True:
        await asyncio.sleep(10)
        if await check_connect(session, url):
            connect_times['curr_time'] = _get_now_formatted()


async def report(session) -> None:
    connect_counter = 0
    connect_state = '🔴 Немає світла'
    current_state = ''
    while True:
        await asyncio.sleep(20)
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
            msg = f'{current_state} : {connect_times["curr_time"]}'
            if _is_day():
                try:
                    await session.get(
                        API_link + f'/sendMessage?chat_id={chat_id}&text={msg}'
                    )
                except:
                    pass


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.datetime.now(tz)
    return now


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%H:%M:%S %d-%m-%Y")


def _is_day() -> bool:
    return 7 < datetime.datetime.now().hour < 24


async def main() -> None:
    tasks = []
    async with aiohttp.ClientSession() as session:

        tasks.append(asyncio.ensure_future(set_time_connect(session, url)))
        tasks.append(asyncio.ensure_future(report(session)))
        await asyncio.gather(*tasks)


asyncio.run(main())
