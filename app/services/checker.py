import asyncio

from app import config
from app.services.utils import get_now_formatted, is_day
from app.models.devices import Devices


connect_times = {'prev_time': '', 'curr_time': ''}

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


async def set_time_connect(session) -> None:

    while True:
        await asyncio.sleep(10)
        for dev in Devices()._get_all_devices():
            if config.PING:
                check_connect = sending_ping_request
            else:
                check_connect = sending_web_request
                url = 'http://' + dev.ip + ':' + config.port + '/'
            print(dev.ip)
            if await check_connect(session, dev.ip):
                connect_times['curr_time'] = get_now_formatted()

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
            if is_day():
                try:
                    await session.get(
                        config.API_link + f'/sendMessage?chat_id={config.chat_id}&text={msg}'
                    )
                except:
                    pass
