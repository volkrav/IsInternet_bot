import asyncio
import asyncpg
from app.data.db_api import get_last_device, update_last_device
import random

N_WORKERS = 1000


async def print_name(pool: asyncpg.Pool, data: dict):
    print(data.get('name'))
    await asyncio.sleep(random.randint(5, 5000) / 1000)
    await update_last_device(pool, data.get('id'))


async def worker(queue: asyncio.Queue, pool):
    while True:
        row = await queue.get()
        # print(f'worker -> {data=}')
        await print_name(pool, row)
        # print('worker done')
        queue.task_done()


async def command_check(session, pool):
    queue = asyncio.Queue(N_WORKERS)

    workers = [asyncio.create_task(worker(queue, pool))
               for _ in range(N_WORKERS)]

    async for data in get_last_device(pool):
        await queue.put(data)

    await queue.join()
    for w in workers:
        w.cancel()
