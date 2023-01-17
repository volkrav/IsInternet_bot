import asyncio
import asyncpg
import aiohttp
import logging

from app.workers.create_workers import preparation_workers
from app.config import load_config, Config

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    logger.info("Starting checker")
    config: Config = await load_config()
    db_connect = {'host': config.db.host,
                  'user': config.db.user,
                  'password': config.db.password,
                  'database': config.db.database}

    async with aiohttp.ClientSession() as session:
        async with asyncpg.create_pool(**db_connect, command_timeout=60) as pool:
            await asyncio.gather(asyncio.create_task(preparation_workers(session, pool, config)))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Stoping checker")
    except Exception as err:
        logger.error(f'Get {err.args}')
