import asyncio
import asyncpg
import aiohttp
import random

from app.data.db_api import update_device, get_last_row
from app.models.devices import Device, create_device
from app.services.checker import _sending_ping_request, check_current_devices_status

N_WORKERS = 100


async def print_name(pool: asyncpg.Pool, device: Device):
    if await _sending_ping_request(None, device.ip):
        print(f'{device.name} ok')
    else:
        print(f'{device.name} BAAAAD')
    # await asyncio.sleep(random.randint(5, 5000) / 1000)
    # await update_device(pool, data.get('id'))


async def worker(session: aiohttp.ClientSession, queue: asyncio.Queue, pool: asyncpg.Pool):
    ids = []
    while True:
        device: Device = await queue.get()
        print(f'\tworker - {device.status=}')
        if device.id not in ids:
            ids.append(device.id)
            await check_current_devices_status(session, pool, device)
            ids.remove(device.id)

        queue.task_done()


async def command_check(session: aiohttp.ClientSession, pool: asyncpg.Pool):
    queue = asyncio.Queue(N_WORKERS)

    workers = [asyncio.create_task(worker(session, queue, pool))
               for _ in range(N_WORKERS)]

    async for raw_device in get_last_row(pool):
        await queue.put(await create_device(raw_device))

    await queue.join()
    for w in workers:
        w.cancel()
