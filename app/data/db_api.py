import asyncpg
import asyncio
import datetime
import pytz


async def db_create_table(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        print('db_connect')
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            "id" serial PRIMARY KEY,
            "name" VARCHAR (255) NOT NULL,
            "last_check" timestamptz NOT NULL
            ) with (
                OIDS=FALSE
            )
        ''')


async def create_n_rows(pool: asyncpg.Pool, n: int):
    async with pool.acquire() as conn:
        for x in range(n):
            await _insert(
                conn,
                'devices',
                {
                    'name': str(x+1),
                    'last_check': get_now_datetime()
                }
            )


async def get_last_device(pool: asyncpg.Pool):
    while True:
        await asyncio.sleep(1)
        async with pool.acquire() as conn:
            async with conn.transaction():
                async for row in conn.cursor(
                    # yield await conn.execute(
                    '''
                select * from devices
                order by "last_check"
                '''
                ):
                    yield row

                # where last_check =
                # (select min(last_check) from devices);

async def update_last_device(pool: asyncpg.Pool, id: int):
    async with pool.acquire() as conn:
        await conn.execute(
            f'UPDATE devices '
            f'SET last_check = $1 '
            f'WHERE id = $2',
            get_now_datetime(),
            id
        )
        # print(f'<update_last_device> OK {id}')


async def _insert(conn: asyncpg.Connection, tablename: str, column_values: dict):
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values())
    placeholders = ', '.join(f'${i}' for i in range(
        1, len(column_values.keys())+1))
    await conn.execute(
        f'INSERT INTO {tablename} '
        f'({columns}) '
        f'VALUES '
        f'({placeholders})',
        *values
    )

TZ = pytz.timezone("Europe/Kiev")


def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ)
    return now
