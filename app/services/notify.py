from app.config import Config
from app.models.devices import Device
from app.misc.utils import get_now_formatted, is_day
from aiohttp import ClientSession


async def notify_user_of_status_change(session: ClientSession,
                                       device: Device,
                                       curr_status,
                                       config: Config) -> None:
    API_link = 'https://api.telegram.org/bot' + config.tg_bot.token
    msg = device.name + '%0A' + \
        await _make_str_status(curr_status) + '%0A' + \
        await get_now_formatted()

    if device.do_not_disturb and not await is_day():
        return
    try:
        await session.get(
            API_link +
            f'/sendMessage?chat_id={device.user_id}&text={msg}',
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
