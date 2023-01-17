import asyncio
import datetime
import os
from typing import NamedTuple

from app.misc.utils import get_now_datetime


class Device(NamedTuple):
    id: int | None
    name: str
    ip: str
    status: str
    do_not_disturb: bool
    notify: bool
    change_date: datetime.datetime | str
    user_id: int
    last_check: datetime.datetime | str


async def create_device(data: dict) -> Device:
    return Device(
        id = data.get('id'),
        name = data.get('name'),
        ip = data.get('ip'),
        status = data.get('status'),
        do_not_disturb = data.get('do_not_disturb'),
        notify = data.get('notify'),
        change_date = data.get('change_date'),
        user_id = data.get('user_id'),
        last_check = data.get('last_check')
    )



# from pydantic import BaseModel

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')


# class Device(BaseModel):
#     id: int
#     name: str
#     ip: str
#     status: str | None
#     do_not_disturb: bool
#     notify: bool
#     change_date: datetime.datetime
#     chat_id: str
#     id: int


# async def get_all_devices() -> Device:
#     loop = asyncio.get_running_loop()

#     dev_dir = await _get_source_dir(RESOURCES_DIR, "devices")
#     async for file_dev in _get_file_from_dir(dev_dir):
#         if file_dev.endswith(".json"):
#             try:
#                 yield await loop.run_in_executor(
#                     None, _sync_open_file_for_read, dev_dir, file_dev)
#             except Exception as err:
#                 pass


# async def update_device_status(dev: Device, status: str) -> None:
#     loop = asyncio.get_running_loop()

#     dev_dir = await _get_source_dir(RESOURCES_DIR, "devices")
#     dev.status = status
#     await loop.run_in_executor(
#         None, _sync_open_file_for_write, dev_dir, dev)


# def _sync_open_file_for_write(dev_dir: str, dev: Device) -> None:
#     with open(os.path.join(dev_dir, dev.name + '.json'), 'w') as f:
#         return f.write(dev.json())


# def _sync_open_file_for_read(dev_dir: str, file_dev: str) -> Device:
#     with open(os.path.join(dev_dir, file_dev)) as data:
#         return Device.parse_raw(data.read())


# async def _get_source_dir(RESOURCES_DIR: str, filename: str) -> str:
#     return os.path.join(RESOURCES_DIR, filename)


# async def _get_file_from_dir(dev_dir: str):
#     for file_dev in os.listdir(dev_dir):
#         yield file_dev
