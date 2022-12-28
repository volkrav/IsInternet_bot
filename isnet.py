import asyncio

from aiohttp import ClientSession

from app.services.checker import check_current_devices_status


async def main() -> None:

    async with ClientSession() as session:
        await asyncio.gather(asyncio.create_task(check_current_devices_status(session)))


asyncio.run(main())
