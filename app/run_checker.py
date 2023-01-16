import asyncio
import asyncpg
import aiohttp
import logging


from app.data.db_api import db_create_table, create_n_rows
from app.data.db_api import get_last_device, update_last_device
from app.checker.check import command_check

logger = logging.getLogger(__name__)


async def run_app(session: aiohttp.ClientSession, pool: asyncpg.Pool):
    logger.info('<run_app> starting')
    await command_check(session, pool)

    # await db_create_table(pool)
    # await create_n_rows(pool, 10000)
    # await command_check()
