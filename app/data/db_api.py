import asyncpg
import asyncio


async def get_last_row(pool: asyncpg.Pool):
    while True:
        await asyncio.sleep(1)
        async with pool.acquire() as conn:
            async with conn.transaction():
                async for row in conn.cursor(
                    '''
                select * from devices
                where notify=true
                order by "last_check"
                '''
                ):
                    yield row


async def update_device(pool: asyncpg.Pool, id: int, column_newvalues: dict):
    columns = [column for column in column_newvalues.keys()]
    placeholders = [f'${i+1}' for i in range(len(column_newvalues.keys()))]
    set_condition = ', '.join([f'{column}={placeholder}'
                               for column, placeholder in zip(columns, placeholders)])
    new_values = [value for value in column_newvalues.values()]
    async with pool.acquire() as conn:
        await conn.execute(
            f'UPDATE devices '
            f'SET {set_condition} '
            f'WHERE id = ${len(placeholders)+1}',
            *new_values,
            id
        )


# async def _insert(conn: asyncpg.Connection, tablename: str, column_values: dict):
#     columns = ', '.join(column_values.keys())
#     values = tuple(column_values.values())
#     placeholders = ', '.join(f'${i}' for i in range(
#         1, len(column_values.keys())+1))
#     await conn.execute(
#         f'INSERT INTO {tablename} '
#         f'({columns}) '
#         f'VALUES '
#         f'({placeholders})',
#         *values
#     )

# async def db_create_table(pool: asyncpg.Pool):
#     async with pool.acquire() as conn:
#         print('db_connect')
#         await conn.execute('''
#             CREATE TABLE IF NOT EXISTS "devices" (
#             "id" serial NOT NULL,
#             "name" varchar(50) NOT NULL,
#             "ip" varchar(50) NOT NULL,
#             "status" varchar(10),
#             "do_not_disturb" BOOLEAN NOT NULL,
#             "notify" BOOLEAN NOT NULL DEFAULT TRUE,
#             "change_date" timestamptz NOT NULL,
#             "user_id" bigint NOT NULL,
#             "last_check" timestamptz NOT NULL,
#             CONSTRAINT "devices_pk" PRIMARY KEY ("id")
#             ) WITH (
#             OIDS=FALSE
#             )
#         ''')


# async def create_n_rows(pool: asyncpg.Pool, n: int):
#     async with pool.acquire() as conn:
#         for x in range(n):
#             await _insert(
#                 conn,
#                 'devices',
#                 {
#                     'name': 'device # ' + str(x+1),
#                     'ip': await _generator_ip(),
#                     'status': '',
#                     'do_not_disturb': True,
#                     'notify': True,
#                     'change_date': await get_now_datetime(),
#                     'user_id': 123456789,
#                     'last_check': await get_now_datetime()
#                 }
#             )


# async def _generator_ip():
#     a = random.randint(0, 255)
#     b = random.randint(0, 255)
#     c = random.randint(0, 255)
#     d = random.randint(0, 255)
#     abcd = [str(i) for i in (a, b, c, d)]
#     return '.'.join(abcd)
