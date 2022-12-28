from app import config
from app.models.devices import Device
from app.services.utils import get_now_formatted, is_day


async def notify_user_of_status_change(session, dev: Device) -> None:

    msg = dev.name + '%0A' + \
        await _make_str_status(dev.status) + '%0A' + \
        get_now_formatted()

    if is_day():
        try:
            await session.get(
                config.API_link +
                f'/sendMessage?chat_id={dev.chat_id}&text={msg}'
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
