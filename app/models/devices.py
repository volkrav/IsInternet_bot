from pydantic import BaseModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')


class Device(BaseModel):
    name: str
    ip: str
    port: str
    state: str
    chat_id: str
    index: int


class Devices(object):
    _instance = None
    _dev_dir = None

    # def _make_folders(self):
    #     if not os.path.exists(self._dev_dir):
    #         os.makedirs(self._dev_dir)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._dev_dir = os.path.join(RESOURCES_DIR, "devices")
        self._devices = self._get_all_devices()

    def __len__(self):
        return len(self._devices)

    def __getitem__(self, position):
        return self._devices[position]

    def _get_all_devices(self):
        devices = []
        for dev in os.listdir(self._dev_dir):
            if dev.endswith(".json"):
                with open(os.path.join(self._dev_dir, dev)) as data:
                    devices.append(Device.parse_raw(data.read()))
        return devices


# dev = Devices()
# for d in dev:
#     print(d)
