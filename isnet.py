from fastapi import FastAPI
import asyncio
import time
import requests

app = FastAPI()
API_link = 'https://api.telegram.org/bot5522301142:AAFpmTT9UiFrqcYibr1F7Mied5CTIRqBWF0'
connect_times = {'prev_time': '', 'curr_time': ''}

@app.get("/")
async def read_root():
    connect_times['curr_time'] = time.ctime()

async def check_connect():
    connect_counter = 0
    connect_state = 'disable'
    current_state = 'disable'
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
            requests.get(API_link + f"/sendMessage?chat_id=234043544&text={current_state}")

tasks = [
    check_connect(),
]

asyncio.gather(*tasks)
