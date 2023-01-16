import asyncio
import asyncpg
import random

from app.data.db_api import update_device, get_last_row
from app.models.devices import Device, create_device
from app.services.checker import _sending_ping_request

N_WORKERS = 1000


async def print_name(pool: asyncpg.Pool, device: Device):
    if await _sending_ping_request(None, device.ip):
        print(f'{device.name} ok')
    else:
        print(f'{device.name} BAAAAD')
    # await asyncio.sleep(random.randint(5, 5000) / 1000)
    # await update_device(pool, data.get('id'))


async def worker(queue: asyncio.Queue, pool):
    while True:
        row = await queue.get()
        await print_name(pool, row)
        queue.task_done()


async def command_check(session, pool):
    queue = asyncio.Queue(N_WORKERS)

    workers = [asyncio.create_task(worker(queue, pool))
               for _ in range(N_WORKERS)]

    async for raw_device in get_last_row(pool):
        await queue.put(await create_device(raw_device))

    await queue.join()
    for w in workers:
        w.cancel()
