import asyncio

# from app import config
# from app.models.devices import Device, get_all_devices, update_device_status
# from app.services.notify import notify_user_of_status_change


# async def check_current_devices_status(session) -> None:
#     timeout = 10
#     while True:
#         await asyncio.sleep(timeout)
#         async for dev in get_all_devices():
#             curr_status = await _get_current_status(session, dev)
#             if dev.status != curr_status:
#                 await update_device_status(dev, curr_status)
#                 await notify_user_of_status_change(session, dev)


async def _sending_ping_request(_, ip) -> bool:
    timeout = 2
    reply = await asyncio.create_subprocess_shell(
        f"ping -c 1 -t {timeout} {ip}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await reply.communicate()
    return reply.returncode == 0


# async def _sending_web_request(session, url) -> bool:
#     try:
#         async with session.get(url) as resp:
#             return resp.status == 200
#     except Exception:
#         return False


# async def _get_current_status(session, dev: Device) -> str:
#     connect_counter = 0
#     number_of_requests = 3
#     if config.PING:
#         check_connect = _sending_ping_request
#         url = dev.ip
#     else:
#         check_connect = _sending_web_request
#         url = 'http://' + dev.ip + ':' + dev.port + '/'
#     while True:
#         if await check_connect(session, url):
#             connect_counter = 0
#             return 'online'
#         else:
#             if connect_counter < number_of_requests:
#                 connect_counter += 1
#             else:
#                 return 'offline'
