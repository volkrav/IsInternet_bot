import asyncio
import asyncpg
import aiohttp
import logging

from app.run_checker import run_app
from app.checker.check import command_check

logger = logging.getLogger(__name__)

db_connect = {'user': 'volodymyr', 'database': 'postgres'}


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    logger.info("Starting checker")

    async with aiohttp.ClientSession() as session:
        async with asyncpg.create_pool(**db_connect, command_timeout=60) as pool:
            await asyncio.gather(asyncio.create_task(run_app(session, pool)))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Stoping checker")
