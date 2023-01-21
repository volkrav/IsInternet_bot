import asyncio
import logging

import aiohttp
import asyncpg

from app.data.db_api import update_device
from app.misc.utils import get_now_datetime
from app.models.devices import Device
from app.services.notify import notify_user_of_status_change

logger = logging.getLogger(__name__)
# async def check_current_devices_status(session) -> None:
#     timeout = 10
#     while True:
#         await asyncio.sleep(timeout)
#         async for dev in get_all_devices():
#             curr_status = await _get_current_status(session, dev)
#             if dev.status != curr_status:
#                 await update_device_status(dev, curr_status)
#                 await notify_user_of_status_change(session, dev)

async def check_current_devices_status(session: aiohttp.ClientSession,
                                       pool: asyncpg.Pool,
                                       device: Device,
                                       config):
    try:
        await update_device(pool,
                            device.id,
                            {
                                'last_check': await get_now_datetime()
                            })
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )
    curr_status = await _get_current_status(session, device)
    if device.status != curr_status:
        await update_device(pool,
        device.id,
        {
            'status': curr_status
        }
        )
        await notify_user_of_status_change(session, device, curr_status, config)


async def _sending_ping_request(_, ip: str) -> bool:
    timeout = 6
    try:
        reply = await asyncio.create_subprocess_shell(
            f"ping -c 1 -t {timeout} {ip}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await reply.communicate()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )

    return reply.returncode == 0


# async def _sending_web_request(session: aiohttp.ClientSession, url: str) -> bool:
#     try:
#         async with session.get(url) as resp:
#             return resp.status == 200
#     except Exception:
#         return False


async def _get_current_status(session, device: Device) -> str:
    connect_counter = 0
    number_of_requests = 5
    while True:
        try:
            if await _sending_ping_request(session, device.ip):
                connect_counter = 0
                return 'online'
            else:
                if connect_counter < number_of_requests:
                    await asyncio.sleep(.5)
                    connect_counter += 1
                else:
                    return 'offline'
        except Exception as err:
            logger.error(
                f'get {err.args}'
            )
