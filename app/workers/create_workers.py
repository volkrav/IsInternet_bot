import logging
import asyncio
import asyncpg
import aiohttp
import random

from app.data.db_api import update_device, get_last_row
from app.models.devices import Device, create_device
from app.services.checker import check_current_devices_status
from app.misc.utils import get_now_datetime

N_WORKERS = 100

logger = logging.getLogger(__name__)


async def worker(session: aiohttp.ClientSession,
                 queue: asyncio.Queue,
                 pool: asyncpg.Pool,
                 id_devices_set: set,
                 config):
    while True:
        device: Device = await queue.get()
        try:
            await update_device(pool,
                                device.id,
                                {
                                    'last_check': await get_now_datetime()
                                })
            await check_current_devices_status(session, pool, device, config)
        except Exception as err:
            logger.error(
                f'get {err.args}'
            )

        # await asyncio.sleep(random.randint(5, 5000) / 1000)
        try:
            id_devices_set.remove(device.id)
        except KeyError:
            print(f'worker : device_ids.remove({device.id}) get KeyError')
        queue.task_done()


async def preparation_workers(session: aiohttp.ClientSession, pool: asyncpg.Pool, config):
    id_devices_set = set()

    queue = asyncio.Queue(N_WORKERS)

    workers = [asyncio.create_task(worker(session, queue, pool, id_devices_set, config))
               for _ in range(N_WORKERS)]

    async for raw_device in get_last_row(pool):
        if raw_device.get('id') not in id_devices_set:
            id_devices_set.add(raw_device.get('id'))
            await queue.put(await create_device(raw_device))

    await queue.join()
    for w in workers:
        w.cancel()
