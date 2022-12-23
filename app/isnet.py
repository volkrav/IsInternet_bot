import asyncio
import time
import aiohttp
import requests

API_link = 'https://api.telegram.org/bot5522301142:AAFpmTT9UiFrqcYibr1F7Mied5CTIRqBWF0'
connect_times = {'prev_time': '', 'curr_time': ''}

async def check_connect(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                return resp.status == 200
        except Exception:
            return False


async def set_time_connect(url):
    while True:
        if await check_connect(url):
            connect_times['curr_time'] = time.ctime()
            print('ok')

async def print_every_3_sec(tik):
    while True:
        await asyncio.sleep(tik)
        print(f'{tik} sec')

async def report():
    connect_counter = 0
    connect_state = 'disable'
    current_state = ''
    while True:
        await asyncio.sleep(5)
        if connect_times['prev_time'] != connect_times['curr_time']:
            connect_times['prev_time'] = connect_times['curr_time']
            connect_counter = 0
            connect_state = 'active'
        else:
            if connect_counter < 5:
                connect_counter += 1
            else:
                connect_state = 'disable'
        if current_state != connect_state:
            current_state = connect_state
            print('requests.get')
            requests.get(API_link + f"/sendMessage?chat_id=234043544&text={current_state}")


async def main():
        tasks = []
        url = 'https://ggle.com'
        tasks.append(asyncio.ensure_future(set_time_connect(url)))
        tasks.append(asyncio.ensure_future(print_every_3_sec(3)))
        tasks.append(asyncio.ensure_future(report()))
        await asyncio.gather(*tasks)





# connect_times['curr_time'] = time.ctime()


#
asyncio.run(main())
