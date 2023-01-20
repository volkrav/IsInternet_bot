import asyncio
import asyncpg
import aiohttp
import logging
import time

from app.workers.create_workers import preparation_workers
from app.config import load_config, Config

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d-%m-%y %H:%M:%S',
        format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='reg_bot.log'
    )
    logger.info("Starting checker")

    config: Config = await load_config()
    db_connect = {'host': config.db.host,
                  'user': config.db.user,
                  'password': config.db.password,
                  'database': config.db.database}
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with asyncpg.create_pool(**db_connect, command_timeout=60) as pool:
                    await asyncio.gather(asyncio.create_task(preparation_workers(session, pool, config)))
        except OSError:
            logger.error('cannot connect to database')
            time.sleep(5)
            continue
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except OSError:
        logger.error('cannot connect to database')
    except KeyboardInterrupt:
        logger.warning("Stoping checker")
    except Exception as err:
        logger.error(f'Checker get {err.args}')
