import asyncio
import asyncpg
import aiohttp
import random

from app.data.db_api import update_device, get_last_row
from app.models.devices import Device, create_device
from app.services.checker import _sending_ping_request, check_current_devices_status

N_WORKERS = 100


async def worker(session: aiohttp.ClientSession,
                 queue: asyncio.Queue,
                 pool: asyncpg.Pool,
                 device_ids: set,
                 config):
    while True:
        device: Device = await queue.get()
        await check_current_devices_status(session, pool, device, config)
        # await asyncio.sleep(random.randint(5, 5000) / 1000)
        try:
            device_ids.remove(device.id)
        except KeyError:
            print(f'worker : device_ids.remove({device.id}) get KeyError')
        queue.task_done()


async def preparation_workers(session: aiohttp.ClientSession, pool: asyncpg.Pool, config):
    device_ids = set()

    queue = asyncio.Queue(N_WORKERS)

    workers = [asyncio.create_task(worker(session, queue, pool, device_ids, config))
               for _ in range(N_WORKERS)]

    async for raw_device in get_last_row(pool):
        if raw_device.get('id') not in device_ids:
            device_ids.add(raw_device.get('id'))
            await queue.put(await create_device(raw_device))

    await queue.join()
    for w in workers:
        w.cancel()
