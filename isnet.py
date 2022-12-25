import asyncio

from aiohttp import ClientSession

from app.services.checker import set_time_connect, report
# from app.services.notify import report


async def main() -> None:
    tasks = []
    async with ClientSession() as session:

        tasks.append(asyncio.create_task(set_time_connect(session)))
        tasks.append(asyncio.create_task(report(session)))
        await asyncio.gather(*tasks)


asyncio.run(main())
