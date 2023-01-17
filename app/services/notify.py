# from app import config
from app.models.devices import Device
from app.misc.utils import get_now_formatted, is_day

API_link = f'https://api.telegram.org/bot' + \
    '5522301142:AAFpmTT9UiFrqcYibr1F7Mied5CTIRqBWF0'


async def notify_user_of_status_change(session,
                                       device: Device,
                                       curr_status) -> None:
    print('start notify_user_of_status_change')
    msg = device.name + '%0A' + \
        await _make_str_status(curr_status) + '%0A' + \
        await get_now_formatted()
    print(msg)
    if await is_day():
        try:
            await session.get(
                API_link +
                f'/sendMessage?chat_id={device.user_id}&text={msg}'
            )
        except Exception as err:
            print(err.args)


async def _make_str_status(status: str) -> str:
    if status == 'online':
        out_status = '🟢 Є світло'
    elif status == 'offline':
        out_status = '🔴 Немає світла'
    else:
        out_status = 'Unknown status'
    return out_status
